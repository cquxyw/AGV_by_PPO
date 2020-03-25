// Auto-generated. Do not edit!

// (in-package scout.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class RL_input_msgs {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.me_x = null;
      this.me_y = null;
      this.me_yaw = null;
      this.me_v = null;
      this.me_w = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('me_x')) {
        this.me_x = initObj.me_x
      }
      else {
        this.me_x = 0.0;
      }
      if (initObj.hasOwnProperty('me_y')) {
        this.me_y = initObj.me_y
      }
      else {
        this.me_y = 0.0;
      }
      if (initObj.hasOwnProperty('me_yaw')) {
        this.me_yaw = initObj.me_yaw
      }
      else {
        this.me_yaw = 0.0;
      }
      if (initObj.hasOwnProperty('me_v')) {
        this.me_v = initObj.me_v
      }
      else {
        this.me_v = 0.0;
      }
      if (initObj.hasOwnProperty('me_w')) {
        this.me_w = initObj.me_w
      }
      else {
        this.me_w = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type RL_input_msgs
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [me_x]
    bufferOffset = _serializer.float64(obj.me_x, buffer, bufferOffset);
    // Serialize message field [me_y]
    bufferOffset = _serializer.float64(obj.me_y, buffer, bufferOffset);
    // Serialize message field [me_yaw]
    bufferOffset = _serializer.float64(obj.me_yaw, buffer, bufferOffset);
    // Serialize message field [me_v]
    bufferOffset = _serializer.float64(obj.me_v, buffer, bufferOffset);
    // Serialize message field [me_w]
    bufferOffset = _serializer.float64(obj.me_w, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type RL_input_msgs
    let len;
    let data = new RL_input_msgs(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [me_x]
    data.me_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [me_y]
    data.me_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [me_yaw]
    data.me_yaw = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [me_v]
    data.me_v = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [me_w]
    data.me_w = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 40;
  }

  static datatype() {
    // Returns string type for a message object
    return 'scout/RL_input_msgs';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '5f2ea7f125f21cbef73d64dd7a90ab98';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
    float64 me_x
    float64 me_y
    float64 me_yaw
    float64 me_v
    float64 me_w
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    # 0: no frame
    # 1: global frame
    string frame_id
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new RL_input_msgs(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.me_x !== undefined) {
      resolved.me_x = msg.me_x;
    }
    else {
      resolved.me_x = 0.0
    }

    if (msg.me_y !== undefined) {
      resolved.me_y = msg.me_y;
    }
    else {
      resolved.me_y = 0.0
    }

    if (msg.me_yaw !== undefined) {
      resolved.me_yaw = msg.me_yaw;
    }
    else {
      resolved.me_yaw = 0.0
    }

    if (msg.me_v !== undefined) {
      resolved.me_v = msg.me_v;
    }
    else {
      resolved.me_v = 0.0
    }

    if (msg.me_w !== undefined) {
      resolved.me_w = msg.me_w;
    }
    else {
      resolved.me_w = 0.0
    }

    return resolved;
    }
};

module.exports = RL_input_msgs;
