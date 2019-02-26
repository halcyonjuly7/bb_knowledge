


import React, {Component} from 'react';
import {inject, observer} from 'mobx-react';

@inject('NavStore')
@observer
class AdminNav extends Component {
    constructor(props) {
        super(props);
        this.nav_store = this.props.NavStore;
    }

    render() {
        return (
        <ul>
            <li id="admin_nav_home" onClick={(e) => this.nav_store.changeTab(e.target.id)}>Home</li>
            <li id="admin_nav_users" onClick={(e) => this.nav_store.changeTab(e.target.id)}>Users</li>
            <li id="admin_nav_questions" onClick={(e) => this.nav_store.changeTab(e.target.id)}>Question</li>
        </ul>
        );
    }




}

export default AdminNav;
