import smtpd
import asyncore
import os

class MainSMTPServer(smtpd.SMTPServer):
    __version__ = 'TEST EMAIL SERVER'
    def process_message(self, peer, mailfrom, rcpttos, data):
        
        import time
        d = os.path.join(os.getcwd(), 'inbox')
        try:
            os.makedirs(d)
        except:
            pass
        ts = time.strftime('%Y%m%d%H%M%S')
        for t in rcpttos:
            fn = os.path.join(d, '%s-%s'%(ts, t))
            print fn
            with open(fn,'w+') as f:
                f.write(data)

        kf = '%-15s'
        print time.strftime('%Y-%m-%d %H:%M:%S')
        print kf%'Client',':', '%s:%s'%peer
        print kf%'Mail From',':', mailfrom
        print kf%'Mail To',':', rcpttos
        print kf%'Mail Lenth',':', len(data)
        print data
        return

if __name__ == "__main__":
    addr = ('0.0.0.0', 25)
    smtp_server = MainSMTPServer(addr, None)
    print 'mail server @ %s:%s'%addr
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()