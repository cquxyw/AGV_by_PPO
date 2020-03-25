
(cl:in-package :asdf)

(defsystem "scout-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "RL_input_msgs" :depends-on ("_package_RL_input_msgs"))
    (:file "_package_RL_input_msgs" :depends-on ("_package"))
  ))