function string_to_array(str, sep=',') {
    return str.split(sep);
}


function array_to_string(arr, sep=',') {
    return arr.join(sep);
}


function json_to_string(json) {
    return JSON.stringify(json);
}


function string_to_json(str) {
    return JSON.parse(str);
}


class ModelManager {
    constructor() {
        this._models = new Map();
        this.init_tags();
    }

    init_tags() {
        let all_tag = document.querySelectorAll('[model]');
        for(const tag of all_tag) {
            let model = tag.getAttribute('model');
            let tags = this._models.get(model);
            if(tags == 'undefined') {
                let tags = [tag];
            } else {
                tags.push(tag);
            }
            this._models.set(tag.getAttribute('model'), tags);
        }
    }

    get_values(model) {
        let values = [];
        let tags = this._models.get(model);
        for(const tag of tags) {
            if(tag.tagName == 'input') {
                let value = tag.getAttribute('value');
            } else {
                let value = tag.textContent;
            }
            values.push(value);
        }
        return values;
    }

    set_value(model, value) {
        let tags = this._models.get(model);
        for(const tag of tags) {
            if(tag.tagName == 'input') {
                let input_type = tag.getAttribute('type');
                if(input_type == 'radio' || input_type == 'checkbox') {
                    // value should be a array.
                    let val = tag.getAttribute('value');
                    if(value.include(val)) {
                        tag.setAttribute('checked', true);
                    } else {
                        tag.setAttribute('checked', false);
                    }
                } else {
                    // value should be a single value.
                    let value = tag.setAttribute('value', value);
                }
            } else {
                tag.textContent = value;
            }
            values.push(value);
        }
    }

    get_data(keys) {

    }

    set_data(data) {

    }
}


class EventManager {
    constructor() {

    }
}


class Wstream {
    static WS_PATH = '/ws';

    constructor (wsurl=null) {
        if(!wsurl) {
            wsurl = this.get_wsurl();
        }
        this._ws = WebSocket(wsurl);
        this._ws.onopen = this._on_open;
        this._ws.onclose = this._on_close;
        this._ws.onmessage = this._on_message;
        this._ws.onerror = this._on_error;
    }

    get_wsurl() {
        let protocal = window.location;
        let host = window.location.host;
        let ws_protocal = protocal == 'http' ? 'ws' : 'wss';
        return ws_protocal + host + this.WS_PATH;
    }

    _on_open(evt) {

    }

    _on_close(evt) {

    }

    _on_message(evt) {

    }

    _on_error(evt) {

    }
}