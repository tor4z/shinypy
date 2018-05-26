/*
ModelIn --- Wstreaam --- ModelOut
client       server      client
*/
'use strict'; 


const Status = {
    
}


function log(msg) {
    console.log('Shiny Log: ' + msg);
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
        if(new.target == ModelManager){
            throw new Error('Can not create model manager object directly.');
        }
        this._models = new Map();
        this.init_tags();
    }

    init_tags() {
        let selector = '[' + this.modelName + ']'
        let allElements = document.querySelectorAll(selector);
        for(const element of allElements) {
            let model = element.getAttribute(this.modelName);
            let elements = this._models.get(model);
            if(elements === undefined) {
                elements = [element];
            } else {
                elements.push(element);
            }
            this._models.set(model, elements);
        }
    }
}



class ModelIn extends ModelManager{
    constructor(wstream) {
        super();
        this._wstream = wstream;
    }

    static get modelName() {return 'model-in';}
    get modelName() {return ModelIn.modelName;}

    init() {
        this.initEventListener();
        let allData = this.getAllData();
        this._wstream.sendJson(allData);
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
                let oldData = data[key];
                let value = ModelIn.getElementValue(element);
                if(oldData === undefined) {
                    data[key] = value;
                } else {
                    if(Array.isArray(oldData)) {
                        data[key].push(value);
                    } else {
                        data[key] = [oldData, value];
                    }
                }
            }
        }
        return data;
    }

    sendElementData(evt) {
        let element = evt.target;
        let data = ModelIn.getElementData(element);
        this._wstream.sendJson(data);
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

    static getElementValue(element) {
        if(element.tagName === 'INPUT') {
            let input_type = element.getAttribute('type');
            if(input_type === 'radio' || input_type == 'checkbox') {
                let model = ModelIn.getElementModel(element);
                let elements = this.getElements(model);
                let value = [];
                for(const element of elements) {
                    if(element.getAttribute('checked')) {
                        value.push(element.getAttribute('value'));
                    }
                }
            } else {
                var value = element.value;
            }
        } else if (element.tagName === 'IMG'){
            var value = element.getAttribute('src');
        } else {
            var value = element.textContent;
        }
        return value;
    }

    static getElementModel(element) {
        return element.getAttribute(ModelIn.modelName);
    }

    static getElementData(element) {
        let data = {}
        let model = ModelIn.getElementModel(element)
        let value = ModelIn.getElementValue(element);
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


class ModelOut extends ModelManager {
    constructor() {
        super();
    }

    static get modelName() {return 'model-out';}
    get modelName() {return ModelOut.modelName;}

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
                        element.setAttribute('checked', false);
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


class Wstream extends WebSocket{
    constructor (wsurl=null, modelOut) {
        super(wsurl)
        log("Connect with websocket to: " + wsurl);
        this._modelOut = modelOut;
        this._buffer = new Buffer();
        this.isClosed = true;
        this.isOpened = false;
        this.onopen = this._onopen
        this.onclose = this._onclose
        this.onmessage = this._onmessage
        this.onerror = this._onerror
    }

    _onopen(evt) {
        this.isOpened = true;
        this.isClosed = false;
        this._sendBuffer();
        log("Wstream opened.");
    }

    _onclose(evt) {
        this.isClosed = true;
        this.isOpened = false;
        log("Wstream closed.");
    }

    _onmessage(evt) {
        let str = evt.data;
        log("Wsrteam recv: " + str)
        let data = string2Json(str);
        this._modelOut.setData(data);
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
        reason: 'Error message'
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
class MessageParser {

}


window.onload = () => {
    let modelOut = new ModelOut();
    let wstream = new Wstream(getWSURL(), modelOut);
    let modelIn = new ModelIn(wstream);
    modelIn.init();
}