import hudson.tasks.Mailer
import jenkins.model.Jenkins
import jenkins.model.JenkinsLocationConfiguration

def location = JenkinsLocationConfiguration.get()
location.setAdminAddress("jenkins@example.com")
location.setUrl("http://127.0.0.1:8080/")
location.save()

def mailer = Jenkins.instance.getDescriptorByType(Mailer.DescriptorImpl.class)
mailer.setSmtpHost("host.docker.internal")
mailer.setSmtpPort("1025")
mailer.setUseSsl(false)
mailer.setCharset("UTF-8")
mailer.save()

println("Configured Jenkins mailer to use Mailpit at host.docker.internal:1025")

