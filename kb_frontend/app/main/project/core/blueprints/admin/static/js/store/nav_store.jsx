import {observable, action, computed} from 'mobx';


class NavStore {
    @observable
    tabs = [
        "home",
        "users",
        "questions"
    ];

    @observable
    current_tab = "home";

    @action
    changeTab = (new_tab) => {
        this.current_tab = new_tab;
    }

}


const nav_store = new NavStore();
export default nav_store;