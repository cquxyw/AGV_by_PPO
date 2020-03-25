#include "serial_port.h"
#include<iostream>

SerialPort::SerialPort(string port, int baude, int databits, \
                       int stopbits, string parity):serial_port_(port), serial_baude_(baude), serial_databits_(databits), \
                                                    serial_stopbits_(stopbits), serial_parity_(parity)
{
    init_flag_ = false;

    while (1)
    {
        if(true == Init())
        {
            break;
        }

        sleep(3);
    }
}


SerialPort::~SerialPort()
{
    Close();
}


bool SerialPort::Init(void)
{
  if(false == init_flag_)
  {
    Init(serial_port_, serial_baude_, 0, serial_databits_, serial_stopbits_, *serial_parity_.data());

    if(true == init_flag_)
    {
      cout<<"Init serial port success!"<<endl;
      return true;
    }
    else
    {
      cout<<"Init serial port failure!"<<endl;
       Close();
      return false;
    }
  }

  return true;
}

/*******************************************************************
* 名称：SerialPortInit()
* 功能：串口初始化
* 入口参数：speed  :  串口速度
*         flow_ctrl  数据流控制
*         databits   数据位   取值为 7 或者8
*         stopbits   停止位   取值为 1 或者2
*         parity     效验类型 取值为N,E,O,,S
*
* 出口参数：        正确返回为true，错误返回为false
*******************************************************************/
bool SerialPort::Init(string port, int speed, int flow_ctrl, int databits, int stopbits, int parity)
{
  int err;

  if(false == OpenPort(port))
  {
    cout<<"Open serial failure!"<<endl;
    init_flag_ = false;
    return false;
  }

  //设置串口数据帧格式
  if (SetParam(speed, flow_ctrl, databits, stopbits, parity) == false)
  {
    cout<<"Set serial param failure!"<<endl;
    init_flag_ = false;
    return false;
  }
  else
  {
    cout<<"Serial Port Info:"<<"port="<<serial_port_.data()<<" baude="<<speed<<" databits="<<databits<< \
          " stopbits="<<stopbits<<" serial_parity="<<parity<<endl;

    init_flag_ = true;
    return  true;
  }
}

/*******************************************************************
* 名称：SerialPortOpen
* 功能： 打开串口
* 入口参数：None
* 出口参数：正确返回为true1，错误返回为false
*******************************************************************/
bool SerialPort:: OpenPort(string port)
{
  serial_fd_ = open(port.c_str(), O_RDWR|O_NOCTTY|O_NDELAY);
  if (false == serial_fd_)
  {
    perror("Can't Open Serial Port");
    return false;
  }
  //恢复串口为阻塞状态
  if(fcntl(serial_fd_, F_SETFL, 0) < 0)
  {
    cout<<"fcntl failed!\n"<<endl;
    return false;
  }
  else
  {
    fcntl(serial_fd_, F_SETFL,0);
  }
  //测试是否为终端设备
  if(0 == isatty(STDIN_FILENO))
  {
    cout<<"standard input is not a terminal device"<<endl;
    return false;
  }
  else
  {
    cout<<"isatty success!"<<endl;
  }
  cout<<"fd->open="<<serial_fd_<<endl;

  return true;
}

/*******************************************************************
* 名称：SerialPortClose
* 功能：关闭串口
* 入口参数:void
* 出口参数：void
*******************************************************************/

void  SerialPort::Close()
{
  init_flag_ = false;
  close(serial_fd_);
  cout<<"Close serial "<<serial_port_<<"!"<<endl;
}

/*******************************************************************
* 名称：SerialPortSet
* 功能：设置串口数据位，停止位和效验位
* 入口参数：speed     串口速度
*         flow_ctrl   数据流控制
*         databits   数据位   取值为 7 或者8
*         stopbits   停止位   取值为 1 或者2
*         parity     效验类型 取值为N,E,O,,S
*出口参数：正确返回为true，错误返回为false
*******************************************************************/
bool SerialPort::SetParam(int speed,int flow_ctrl,int databits,int stopbits,int parity)
{
  int i;
  int status;
  int speed_arr[] = { B115200, B38400, B19200, B9600, B4800, B2400, B1200, B300};
  int name_arr[] = {115200, 38400, 19200,  9600,  4800,  2400,  1200,  300};
 //int speed_arr[] = { B115200, B19200, B9600, B4800, B2400, B1200, B300};
 // int name_arr[] = {115200, 19200,  9600,  4800,  2400,  1200,  300};

  struct termios options;

  /*tcgetattr(fd,&options)得到与fd指向对象的相关参数，并将它们保存于options,该函数还可以测试配置是否正确，该串口是否可用等。若调用成功，函数返回值为0，若调用失败，函数返回值为1.
  */
  if( tcgetattr(serial_fd_,&options)  !=  0)
  {
    perror("SetupSerial 1");
    return false;
  }

  //设置串口输入波特率和输出波特率
  for ( i= 0;  i < sizeof(speed_arr) / sizeof(int);  i++)
  {
    if (speed == name_arr[i])
    {
      cfsetispeed(&options, speed_arr[i]);
      cfsetospeed(&options, speed_arr[i]);
    }
  }

  //修改控制模式，保证程序不会占用串口
  options.c_cflag |= CLOCAL;
  //修改控制模式，使得能够从串口中读取输入数据
  options.c_cflag |= CREAD;

  //设置数据流控制
  switch(flow_ctrl)
  {
    case 0 ://不使用流控制
        options.c_cflag &= ~CRTSCTS;
        break;
    case 1 ://使用硬件流控制
        options.c_cflag |= CRTSCTS;
        break;
    case 2 ://使用软件流控制
        options.c_cflag |= IXON | IXOFF | IXANY;
        break;
  }
  //设置数据位
  //屏蔽其他标志位
  options.c_cflag &= ~CSIZE;
  switch (databits)
  {
    case 5:
        options.c_cflag |= CS5;
        break;
    case 6:
        options.c_cflag |= CS6;
        break;
    case 7:
        options.c_cflag |= CS7;
        break;
    case 8:
        options.c_cflag |= CS8;
        break;
    default:
        fprintf(stderr,"Unsupported data size\n");
        return false;
  }
  //设置校验位
  switch (parity)
  {
    case 'n':
    case 'N': //无奇偶校验位。
        options.c_cflag &= ~PARENB;
        options.c_iflag &= ~INPCK;
        break;
    case 'o':
    case 'O'://设置为奇校验
        options.c_cflag |= (PARODD | PARENB);
        options.c_iflag |= INPCK;
        break;
    case 'e':
    case 'E'://设置为偶校验
        options.c_cflag |= PARENB;
        options.c_cflag &= ~PARODD;
        options.c_iflag |= INPCK;
        break;
    case 's':
    case 'S': //设置为空格
        options.c_cflag &= ~PARENB;
        options.c_cflag &= ~CSTOPB;
        break;
    default:
        fprintf(stderr,"Unsupported parity\n");
        return false;
  }
  // 设置停止位
  switch (stopbits)
  {
    case 1:
        options.c_cflag &= ~CSTOPB; break;
    case 2:
       options.c_cflag |= CSTOPB; break;
    default:
        fprintf(stderr,"Unsupported stop bits\n");
        return false;
  }

  //修改输出模式，原始数据输出
  options.c_oflag &= ~OPOST;

  options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
  //options.c_lflag &= ~(ISIG | ICANON);

  //设置等待时间和最小接收字符
  options.c_cc[VTIME] = 1; /* 读取一个字符等待1*(1/10)s */
  options.c_cc[VMIN] = 1; /* 读取字符的最少个数为1 */

  //如果发生数据溢出，接收数据，但是不再读取 刷新收到的数据但是不读
  tcflush(serial_fd_, TCIFLUSH);

  //Rev spical char 0x13...
 // options.c_cflag &= ~(ICRNL | IXON);
  options.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);

  //激活配置 (将修改后的termios数据设置到串口中）
  if (tcsetattr(serial_fd_, TCSANOW, &options) != 0)
  {
    perror("com set error!\n");
    return false;
  }

  return true;
}


/*******************************************************************
* 名称：SerialPortRecv
* 功能：接收串口数据
* 入口参数：rcv_buf:接收串口中数据存入rcv_buf缓冲区中
*         data_len:缓冲区长度
*         len:接收数据长度
* 出口参数：正确返回为true，错误返回为false
*******************************************************************/
bool SerialPort::Recv(char *rcv_buf,int rev_buff_len, int *len, int time_out)
{
  int fs_sel;
  fd_set fs_read;

  struct timeval time;

  FD_ZERO(&fs_read);
  FD_SET(serial_fd_, &fs_read);

  time.tv_sec = time_out;
  time.tv_usec = 0;

  //使用select实现串口的多路通信
  fs_sel = select(serial_fd_+1, &fs_read, NULL, NULL, &time);
  //printf("fs_sel = %d\n",fs_sel);
  if(0 == fs_sel)
  {
     cout<<"Serial port time out!"<<endl;
  }
  else if(-1 == fs_sel)
  {
    cout<<"Serial port error!"<<endl;
    init_flag_ = false;
    return false;
  }
  else
  {
    *len = read(serial_fd_, rcv_buf, rev_buff_len);
    return true;
  }
}

/********************************************************************
* 名称：SerialPortSend
* 功能：发送数据
* 入口参数：send_buf:存放串口发送数据
*         data_len:一帧数据的个数
* 出口参数：正确返回为true，错误返回为0
*******************************************************************/
bool SerialPort::Send(char *send_buf,int data_len)
{
  int len = 0;

  len = write(serial_fd_, send_buf, data_len);
  if (len == data_len )
  {
    return true;
  }
  else
  {
    tcflush(serial_fd_, TCOFLUSH);
    return false;
  }
}
