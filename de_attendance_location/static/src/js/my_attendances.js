odoo.define('de_attendance_location.my_attendances', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var AttendanceMyMainMenuLocation = require('hr_attendance.my_attendances')
    var core = require('web.core');
    var field_utils = require('web.field_utils');


    var MyAttendances = AttendanceMyMainMenuLocation.extend({
        contentTemplate: 'DeAttendanceMyMainMenuLocation',

        events: {
            "click .o_hr_attendance_sign_in_out_icon": _.debounce(function () {
                this._onUpdateAttendance();
            }, 200, true),
        },
        getLocation: function (callback) {
            var self = this;
            if (navigator.geolocation) {
                var lat_lng = navigator.geolocation.getCurrentPosition(function (position) {
                    callback(position.coords.latitude, position.coords.longitude);
                });
            }
        },
        _onUpdateAttendance: function () {
            var self = this;
            var check_in_out_msg = $('#check_in_out_msg').val()
            console.log(check_in_out_msg)
            self.getLocation((lat, lng) => {
                self._rpc({
                    model: 'hr.employee',
                    method: 'update_attendance_data',
                    args: [[self.employee.id], self.employee.attendance_state, check_in_out_msg,
                        lat, lng],
                }).then(function (result) {
                    return self.update_attendance();
                });
            });
        }
    });

    core.action_registry.add('de_attendance_location_my_attendances', MyAttendances);

    return MyAttendances;

});

odoo.define('googlemap.FieldGoogleMap', function (require) {
    "use strict";
    var field_registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var FieldGoogleMap = AbstractField.extend({
        events: {
            'click a.view_attn': '_showEmployeeAttendance',
        },
        template: 'FieldGoogleMap',
        start: function () {
            var self = this;
            self.init_map();
            return this._super();
        },

        _showEmployeeAttendance: function(e){
            e.preventDefault();
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                name: 'Attendances',
                res_model: 'hr.attendance',
                views: [[false, 'list']],
                domain: [['employee_id', '=', parseInt(e.target.id)]],
                target: 'current'
            });
        },

        init_map: function () {
            var self = this;
            var markers = [];
            var locations = eval(this.value);
            this.map = new google.maps.Map($(this.el).find('#tung_googlemap')[0], {
                center: { lat: 0, lng: 0 },
                zoom: 2,
                disableDefaultUI: true,
            });
            var i, j;
            for (i = 0; i < locations.length; i++) {
                for (j = 0; j < locations[i].length; j++) {

                    var marker = new google.maps.Marker({
                        position: new google.maps.LatLng(parseFloat(locations[i][j][0]), parseFloat(locations[i][j][1])),
                        map: this.map,
                        title: locations[i][j][2],
                    });
                    var infowindow = new google.maps.InfoWindow()

                    var content = `     <img src="/web/image/hr.employee/${locations[i][j][3]}/image_128" width="50" height="50">
                                        <b>${locations[i][j][2]}</b>
                                        <br/>
                                        <a href="javascript:void(0)" t-att-data-id="${locations[i][j][3]}" class="view_attn" id="${locations[i][j][3]}">View Attendance</a>
                                   `

                    google.maps.event.addListener(marker, 'click', (function (map, marker, content, infowindow) {
                        return function () {
                            infowindow.setContent(content);
                            infowindow.open(map, marker);
                        };
                    })(this.map, marker, content, infowindow));
                }
            }
        }
    });

    field_registry.add('googlemap', FieldGoogleMap);

    return {
        FieldGoogleMap: FieldGoogleMap,
    };
});
