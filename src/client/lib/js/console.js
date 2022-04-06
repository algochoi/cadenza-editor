let console = (function (oldCons) {
    return {
        logString: function (item) {
            oldCons.log(item);
            consoleMessages.push({
                item,
            });
            oldCons.log(consoleMessages);
        },
        log: function (text) {
            const args = Array.from(arguments);
            return this.logString(text);
        }
    }
})(window.console);