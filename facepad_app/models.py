from django.db import models


# Create your models here.

class SimpleUser(models.Model):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["name", "date"]

    name = models.CharField(max_length=100, verbose_name="Username")
    password = models.CharField(max_length=50, verbose_name="Password")
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Avatar", blank=True, null=True)
    date = models.DateField(verbose_name="Date of birth")
    friend = models.ManyToManyField('SimpleUser', verbose_name="Friends",
                                    related_name='related_friends', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-date", "-pk"]

    content = models.TextField(max_length=1000, verbose_name="Post content")
    date = models.DateField(verbose_name="Posted on", auto_now=True)
    user = models.ForeignKey(to="SimpleUser", related_name="posts", verbose_name="User")
    section = models.ForeignKey(to="Section", related_name="posts", verbose_name="Section")

    def __str__(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content[:len(self.content)]

    def my_section(self):
        return self.section.id

    def count(self):
        return len(self.likes.all())

    def comments_count(self):
        return len(self.comments.all())


class Comment(models.Model):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-date', '-pk']

    user = models.ForeignKey(to="SimpleUser", related_name="comments", verbose_name="User")
    post = models.ForeignKey(to="Post", related_name="comments", verbose_name="Post", null=True, blank=True)
    content = models.CharField(max_length=300, verbose_name="Comment")
    date = models.DateField(verbose_name="Commented on")

    def my_section(self):
        return self.post.my_section()

    def __str__(self):
        return self.content[:10] + "..." if len(self.content) > 10 else self.content[:len(self.content)]

    def count(self):
        return len(self.likes.all())


class Likes(models.Model):
    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = "Likes"

    user = models.ForeignKey(to="SimpleUser", related_name="likes", verbose_name="User")
    post = models.ForeignKey(to="Post", related_name="likes", verbose_name="Post", blank=True, null=True)
    comment = models.ForeignKey(to="Comment", related_name="likes", verbose_name="Comment", blank=True, null=True)


class Section(models.Model):
    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    name = models.CharField(max_length=100, verbose_name="Section name")
    section = models.OneToOneField('Section', related_name='sub_section', blank=True, null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["date", 'pk']

    content = models.TextField(max_length=500, verbose_name="Message content")
    date = models.DateField(verbose_name="Message date")
    senderUser = models.ForeignKey(to="SimpleUser", related_name="messageSender", verbose_name="Sender")
    receiverUser = models.ForeignKey(to="SimpleUser", related_name="messageReceiver", verbose_name="Receiver")

    def __str__(self):
        return self.id
