(function (debug) {
    var w = debug.documentElement.offsetWidth,
        t = debug.createTreeWalker(debug.body, NodeFilter.SHOW_ELEMENT),
        b;
    while (t.nextNode()) {
        b = t.currentNode.getBoundingClientRect();
        if (b.right > w || b.left < 0) {
            t.currentNode.style.setProperty('outline', '1px dotted red', 'important');
            console.log(t.currentNode);
        }
    };
}(document));
