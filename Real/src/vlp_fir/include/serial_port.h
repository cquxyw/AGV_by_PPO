#ifndef SERIALPORT_H
#define SERIALPORT_H

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>

#include <string>

using namespace std;

class SerialPort
{
public:
    SerialPort(string port, int baude, int databits, \
               int stopbits, string parity);
    virtual ~SerialPort();

private:
    int serial_fd_;
    int init_flag_;

    string serial_port_;
    int serial_baude_;
    int serial_databits_;
    int serial_stopbits_;
    string serial_parity_;

    bool OpenPort(string port);
    void Close();
    bool SetParam(int speed, int flow_ctrl, int databits, int stopbits, int parity);


public:
    bool Init(void);
    bool Init(string port, int speed, int flow_ctrl, int databits, int stopbits, int parity);
    bool Recv(char *rcv_buf, int rev_buff_len, int *len, int time_out);
    bool Send(char *send_buf,int data_len);
};

#endif // SERIALPORT_H
