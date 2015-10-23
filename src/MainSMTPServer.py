import smtpd
import asyncore
import os
import email
def parsemail(mail, savename):
    prefix = savename
    mails = []
    names = []
    def parsesingle(mail):
        if mail.is_multipart():
            for m in mail.get_payload():
                parsesingle(m)
            return
        name = mail.get_param("name")
        if name:
            # attachment
            name = email.Header.decode_header(email.Header.Header(name))[0][0]
        charset = mail.get_content_charset()
        contenttype = mail.get_content_type()
        data = mail.get_payload(decode=True)
        if charset and contenttype and contenttype.upper().startswith('TEXT'):
            data = unicode(data, str(charset), "ignore").encode('utf8', 'replace')
        if name:
            # save attachment
            names.append(name)
            attindex = len(names)
            try:
                f = open(u'%s.atach.%d.%s'%(prefix, attindex, fname), 'wb')
            except:
                f = open('%s.atach.%d'%(prefix, attindex), 'wb')
            f.write(data)
            f.close()
        else:
            mails.append(data)
    parsesingle(mail)
    mailtext = '\r\n\r\n'.join(mails)
    with open(savename, 'wb') as f:
        f.write(mailtext)
    return mailtext


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
        mail = email.message_from_string(data)
        mailtext = parsemail(mail, os.path.join(d, '%s.txt'%ts))
        for t in rcpttos:
            fn = os.path.join(d, '%s-%s'%(ts, t))
            print fn
            with open(fn,'wb') as f:
                f.write(data)

        kf = '%-15s'
        print time.strftime('%Y-%m-%d %H:%M:%S')
        print kf%'Client',':', '%s:%s'%peer
        print kf%'Mail From',':', mailfrom
        print kf%'Mail To',':', rcpttos
        print kf%'Mail Lenth',':', len(data)
        print mailtext
        return

if __name__ == "__main__":
    addr = ('0.0.0.0', 25)
    smtp_server = MainSMTPServer(addr, None)
    print 'mail server @ %s:%s'%addr
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()