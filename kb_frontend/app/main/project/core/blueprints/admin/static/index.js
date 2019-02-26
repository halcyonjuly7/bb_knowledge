import React from 'react';
import ReactDOM from "react-dom";
import AdminNav from "./js/admin_nav";
import AdminBody from "./js/admin_body";

import {Provider} from 'mobx-react';
import NavStore from './js/store/nav_store';

const nav = <Provider NavStore={NavStore}>
    <AdminNav/>
</Provider>

const body =
    <Provider NavStore={NavStore}>
        <AdminBody/>
    </Provider>


ReactDOM.render(nav, document.getElementById("admin_nav"));
ReactDOM.render(body, document.getElementById("body_container"));

