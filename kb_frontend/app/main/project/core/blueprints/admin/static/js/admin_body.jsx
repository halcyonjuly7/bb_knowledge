import React, {Component} from "react";
import {inject, observer} from "mobx-react";
import AdminHome from './admin_home';
import AdminModel from './admin_models';


@inject('NavStore')
@observer
export default class AdminComponent extends Component {
    constructor(props) {
        super(props)
        this.nav_store = this.props.NavStore;
    }

    render() {
        if(this.nav_store.current_tab.toLowerCase() === "admin_nav_home") {
            return <AdminHome/>;
        }
        return <AdminModel/>;

    }

}