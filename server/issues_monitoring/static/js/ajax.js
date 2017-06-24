/*
 *    This program is free software: you can redistribute it and/or
 *    modify
 *    it under the terms of the GNU Affero General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

function ajax(url, obj, callback, err_callback) {
    var xml_http = new XMLHttpRequest();

    xml_http.onreadystatechange = function() {
        var READY = 4,
            OK = 200;
        
        if (this.readyState === READY && this.status === OK) {
            var data = this.responseText;
            console.log(data, data !== "OK")
            if (data !== "OK")
                callback(data);
            else
                callback();
        } else if (this.status >= 500) {
            if (typeof(err_callback) == typeof(ajax))
                err_callback();
        }
    };

    xml_http.open("POST", url, true);
    xml_http.onerror = err_callback;
        
    if (typeof(obj) !== 'undefined' && obj !== null) {
        obj = JSON.stringify(obj);
        xml_http.setRequestHeader('Content-Type',
                                  'application/json;charset=UTF-8');
    }
    
    xml_http.send(obj);
}
