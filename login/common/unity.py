import random, string
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


class Imagfont(object):
    pass


class ImagCode:
    # 生成图片颜色
    def rand_color(self):
        red = random.randint(32, 127)
        green = random.randint(32, 127)
        blue = random.randint(32, 127)
        return red, green, blue
    # 生成随机字符串
    def gen_text(self):
        list = random.sample(string.ascii_letters+string.digits, 4)
        return  ''.join(list)

    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width/2)
            y1 = random.randint(0, height/2)
            x2 = random.randint(0, width)
            y2 = random.randint(height/2, height)
            draw.line(((x1, y1),(x2, y2)), fill='black', width=2)
    # 绘制图片
    def draw_very_code(self):
        code = self.gen_text()
        width, height = 120, 50
        im = Image.new('RGB', (width, height), 'white')
        font = ImageFont.truetype(font = 'arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 2, width, height)
        im.show()
        return im, code

    # 生成图片并发给控制器
    def get_code(self):
        image, code = self.draw_very_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
def send_email(receiver, ecode):
    sender = 'xiaxia <2542568686@qq.com>'
    content = f"<br/>欢迎注册夏夏的网站，您的邮箱验证码为:" \
                  f"<span style='color:red;font-size:20px;'> {ecode}</span>" \
                  f",请复制到注册窗口,thanks <br/>"


    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header('xiaxia注册验证码', 'utf-8')
    message['From'] = sender
    message['To'] = receiver  # 收件人

    smtpobj = SMTP_SSL('smtp.qq.com')  # 与qq服务器连接
    smtpobj.login(user='2542568686@qq.com', password='ppxjkxjqgenweccg')
    smtpobj.sendmail(sender, receiver, str(message))
    smtpobj.quit()

def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)