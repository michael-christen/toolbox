import Toybox.Lang;
import Toybox.WatchUi;

class garmin_hello_worldDelegate extends WatchUi.BehaviorDelegate {

    function initialize() {
        BehaviorDelegate.initialize();
    }

    function onMenu() as Boolean {
        WatchUi.pushView(new Rez.Menus.MainMenu(), new garmin_hello_worldMenuDelegate(), WatchUi.SLIDE_UP);
        return true;
    }

}