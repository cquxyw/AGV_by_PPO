
(cl:in-package :asdf)

(defsystem "vlp_fir-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "send_msgs" :depends-on ("_package_send_msgs"))
    (:file "_package_send_msgs" :depends-on ("_package"))
  ))