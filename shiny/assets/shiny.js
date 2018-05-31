/*
                ModelManager
(model-in, model-out, model-layout, model-button)
                 /  |  \
                /   |   \
               /    |    \
              /     |     \
             /      |      \
            /       |       \
     ModelIn --- Wstreaam --- ModelOut
    client       server      client
*/
'use strict'; 


const Status = {
    SUCCESS: 0,
    ERROR: 1
}


const Method = {
    GET: 'GET',
    SET: 'SET',
    EXEC: 'EXEC'
}


const Model = {
    IN: 'model-in',
    OUT: 'model-out',
    LAYOUT: 'model-layout',
    BUTTON: 'model-button'
}


function log(msg) {
    console.log('Shiny Log: ' + msg);
}


function error(msg) {
    console.error('Shiny error: ' + msg);
}


function warn(msg) {
    console.warn('Shiny warn: ' + msg);
}


function string2Array(str, sep=',') {
    return str.split(sep);
}


function array2String(arr, sep=',') {
    return arr.join(sep);
}


function json2String(json) {
    return JSON.stringify(json);
}


function string2Json(str) {
    return JSON.parse(str);
}


function getWSURL() {
    let protocal = window.location.protocol;
    let host = window.location.host;
    let ws_protocal = (protocal === 'http:') ? 'ws' : 'wss';
    return ws_protocal + '://' + host;
}


class ModelManager {
    constructor() {
        this.in_models = new Map();
        this.out_models = new Map();
        this.layout_models = new Map();
        this.button_models = new Map();
        this.init_models();
    }

    getModels(key) {
        switch (key) {
            case 'IN':
                return this.in_models;
            case 'OUT':
                return this.out_models;
            case 'LAYOUT':
                return this.layout_models;
            case 'BUTTON':
                return this.button_models;
            default:
                throw new Error('Invalid model key.');
        }
    }

    init_models() {
        for(let key in Model) {
            let modelName = Model[key];
            let selector = '[' + modelName + ']';
            let models = this.getModels(key);

            let allElements = document.querySelectorAll(selector);
            for(const element of allElements) {
                let model = element.getAttribute(modelName);
                let elements = models.get(model);
                if(elements === undefined) {
                    elements = [element];
                } else {
                    elements.push(element);
                }
                models.set(model, elements);
            }
        }
    }

    query(model, keys) {
        if(!Array.isArray(keys)) {
            throw new Error("array required.");
        }

        let models = this.getModels(model);
        let data = {};
        for(let key of keys) {
            data[key] = models.get(key);
        }
        return data;
    }
}


class ModelIn{
    constructor(models, wstream) {
        this._models = models.in_models;
        this._wstream = wstream;
    }

    init() {
        let allData = this.getAllData();
        let msg = new Message();
        msg.method = Method.EXEC;
        msg.data = allData;
        this._wstream.sendMsg(msg);
        this.initEventListener();
    }

    initEventListener() {
        for(const key of this._models.keys()) {
            let elements = this._models.get(key);
            for(let element of elements) {
                element.addEventListener('change', this.sendElementData.bind(this));
            }
        }
    }

    getAllData() {
        let data = {}
        for(const key of this._models.keys()) {
            let elements = this._models.get(key);
            for(const element of elements) {
                if(!(key in data)) {
                    let value = this.getElementValue(element);
                    data[key] = value;
                }
            }
        }
        return data;
    }

    sendElementData(evt) {
        let element = evt.target;
        let data = this.getElementData(element);
        let msg = new Message();
        msg.data = data;
        msg.method = Method.EXEC;
        this._wstream.sendMsg(msg);
    }

    getValues(model) {
        let values = [];
        let elements = this.getElements(model);
        for(const element of elements) {
            value = this.getElementValue(element);
            values.push(value);
        }
        return values;
    }

    getElements(model) {
        return this._models.get(model);
    }

    getElementValue(element) {
        if(element.tagName === 'INPUT') {
            let input_type = element.getAttribute('type');
            if(input_type === 'radio' || input_type == 'checkbox') {
                let model = this.getElementModel(element);
                let elements = this.getElements(model);
                if(input_type === 'radio') {
                    var value = '';
                    for(const element of elements) {
                        if(element.checked) {
                            value = element.value;
                        }
                    }
                } else {
                    var value = [];
                    for(const element of elements) {
                        if(element.checked) {
                            value.push(element.value);
                        }
                    }
                }
            } else {
                var value = element.value;
            }
        } else if (element.tagName === 'IMG'){
            var value = element.getAttribute('src');
        } else if(element.tagName === 'SELECT') {
            var value = '';
            let elements = element.children;
            for(let element of elements) {
                if(element.selected) {
                    value = element.value;
                }
            }
        } else {
            var value = element.textContent;
        }
        return value;
    }

    getElementModel(element) {
        return element.getAttribute(Model.IN);
    }

    getElementData(element) {
        let data = {}
        let model = this.getElementModel(element)
        let value = this.getElementValue(element);
        data[model] = value;
        return data;
    }

    getData(...keys) {
        data = {};
        for(const key of keys) {
            data[key] = this.getValues(key);
        }
        return data;
    }
}


class ModelOut {
    constructor(models) {
        this._models = models.out_models;
    }

    setValue(model, value) {
        var elements = this._models.get(model);
        if(elements === undefined) {
            return
        }

        for(const element of elements) {
            let tagName = element.tagName;
            if(tagName === 'INPUT') {
                let input_type = element.getAttribute('type');
                if(input_type === 'radio' || input_type == 'checkbox') {
                    // value should be a array.
                    let val = element.getAttribute("value");
                    if(value.include(val)) {
                        element.setAttribute('checked', true);
                    } else {
                        element.removeAttribute('checked');
                    }
                } else {
                    // value should be a single value.
                    let value = element.setAttribute('value', value);
                }
            } else if(tagName === 'IMG'){
                element.setAttribute('src', value);
            } else {
                element.textContent = value;
            }
        }
    }

    setData(data) {
        for(const key in data) {
            this.setValue(key, data[key]);
        }
    }
}


class Buffer {
    constructor() {
        this.buffer = new Array()
    }

    push(data) {
        if(data != undefined) {
            this.buffer.push(data)
        }
    }

    get size() {
        return this.buffer.length;
    }

    pop() {
        if(this.size > 0) {
            return this.buffer.pop();
        } else {
            throw new Error("Buffer empty.");
        }
    }
}


class WStream extends WebSocket{
    constructor (wsurl, modelOut, models) {
        super(wsurl)
        log("Connect with websocket to: " + wsurl);
        this._modelOut = modelOut;
        this._buffer = new Buffer();
        this.isClosed = true;
        this.isOpened = false;
        this.onopen = this._onopen;
        this.onclose = this._onclose;
        this.onmessage = this._onmessage;
        this.onerror = this._onerror;
        this._models = models;
    }

    _onopen(evt) {
        this.isOpened = true;
        this.isClosed = false;
        this._sendBuffer();
        log("WStream opened.");
    }

    _onclose(evt) {
        this.isClosed = true;
        this.isOpened = false;
        log("WStream closed.");
    }

    _onmessage(evt) {
        let str = evt.data;
        log("WSrteam recv: " + str)
        let msg = new Message(str);
        this.resolveMsg(msg);
    }

    resolveMsg(msg) {
        if(!msg.success) {
            error('Error' + msg.reason);
        }

        if(msg.method === Method.SET) {
            this._modelOut.setData(msg.data);
        } else if(msg.method === Method.GET) {
            let data = this._models.query('IN', msg.keys);
            let result = new Message()
            result.data = data;
            this.sendMsg(result);
        }
    }

    _onerror(evt) {

    }

    sendJson(data) {
        let str = json2String(data);
        this.sendStr(str);
    }

    sendStr(str) {
        this._sendStr(str);
    }

    sendMsg(msg) {
        this.sendStr(msg.stringify());
    }

    _sendBuffer() {
        if(this.isOpened) {
            while(true) {
                try {
                    let str = this._buffer.pop();
                    this._sendStr(str);
                } catch(err) {
                    log(err);
                    return
                }
            }
        }
    }

    _sendStr(str) {
        if(!this.isOpened) {
            this._buffer.push(str);
        } else {
            log("Wsrteam send: " + str)
            super.send(str);
        }
    }
}


/*
All message should be a json string.
Get:
    query msg:
    {
        method: 'GET',
        data: {
            keys: ['key1', 'key2', 'key3', ...]
        }
    }
    responses msg:
    {
        status: status_code,
        reason: 'Error message',
        data: {
            key: value (single value or array of value)
        }
    }

Set:
    set msg
    {
        method: 'SET',
        data: {}
    }
    responses msg:
    {
        status: status_code,
        reason: 'Error message',
    }

Execute:
    {
        method: 'EXEC',
        data: {}
    }

    {
        status: status_code,
        reason: 'Error message',
        data: {}
    }
*/
class Message {
    constructor(msg=null) {
        if(msg === null) {
            this.msg = {};
        } else if(typeof msg === 'string') {
            this.msg = string2Json(msg);
        } else if(typeof msg === 'object') {
            this.msg = msg;
        }
    }

    get status() {
        return this.msg.status;
    }

    set status(status) {
        this.msg.status = status;
    }

    get success() {
        if(this.msg.status === Status.SUCCESS) {
            return true;
        } else {
            return false;
        }
    }

    get reason() {
        return this.msg.reason;
    }

    set reason(reason) {
        this.msg.reason = reason;
    }

    get method() {
        return this.msg.method;
    }

    set method(method) {
        this.msg.method = method;
    }

    get data() {
        return this.msg.data;
    }

    set data(data) {
        this.msg.data = data;
    }

    get keys() {
        // Work only method is GET
        return this.msg.data.keys;
    }

    add(key, value) {
        if(this.msg.data === undefined) {
            this.msg.data = {};
        }

        this.msg.data[key] = value;
    }

    _msgChecker() {
        if(this.msg.status === undefined) {
            this.msg.status = Status.SUCCESS;
        }

        if(this.msg.reason === undefined) {
            this.msg.reason = '';
        }
    }

    stringify() {
        this._msgChecker();
        return json2String(this.msg);
    }
}


class Alert {
    static success(msg) {

    }

    static error(msg) {

    }

    static warn(msg) {
        
    }
}


window.onload = () => {
    let models = new ModelManager();
    let modelOut = new ModelOut(models);
    let wstream = new WStream(getWSURL(), modelOut, models);
    let modelIn = new ModelIn(models, wstream);
    modelIn.init();
}