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

function ajax(url) {
    var xml_http = new XMLHttpRequest();

    xml_http.onreadystatechange = function() {
        var READY = 4,
            OK = 200;
        
        if (this.readyState === READY && this.status === OK) {
            window.history.pushState('', '', this.responseURL);
            location.reload();
        } else if (this.status >= 500) {
            location.reload();
        }
    };

    xml_http.open("POST", url, true);
    xml_http.send();
}
function ajax_get(url) {
    var xml_http = new XMLHttpRequest();

    xml_http.onreadystatechange = function() {
        var READY = 4,
            OK = 200;
        
        if (this.readyState === READY && this.status === OK) {
            window.history.pushState('', '', this.responseURL);
            location.reload();
        } else if (this.status >= 500) {
            location.reload();
        }
    };

    xml_http.open("GET", url, true);
    xml_http.send();
}