using Toybox.WatchUi as WatchUi;
using Toybox.Graphics as Graphics;

class HelloWorldApp extends WatchUi.WatchAppBase {
    function initialize() {
        WatchUi.WatchAppBase.initialize();
    }

    function onStart() {
    }

    function getInitialView() {
        return new HelloWorldView();
    }
}

class HelloWorldView extends WatchUi.View {
    function initialize() {
        View.initialize();
    }

    function onLayout(dc) {
        View.onLayout(dc);
        setLayout(WatchUi.loadResource(WatchUi.Layouts.LAYOUT));
        var label = findDrawableById("mainLabel");
        label.setText("Hello, World!");
    }

    function onUpdate(dc) {
        View.onUpdate(dc);
    }
}
