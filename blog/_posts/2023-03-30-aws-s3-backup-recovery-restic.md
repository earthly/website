---
title: "AWS S3 Backup and Recovery With Restic"
categories:
  - Tutorials
toc: true
author: Saka-Aiyedun Segun
editor: Bala Priya C

internal-links:
 - AWS
 - Backup
 - Restic
 - Amazon
 - S3 Bucket
excerpt: |
    Learn how to use Restic, an open-source backup software, to protect your valuable data from potential threats. This tutorial will guide you through the process of configuring Restic on your Unix machine, backing up data to an AWS S3 bucket, restoring data, and automating backups with cron jobs. Don't wait any longer, start securing your data today!
last_modified_at: 2023-07-19
---
**This tutorial offers a step-by-step guide on using Restic for backups. For Restic users, Earthly streamlines the build process. [Check it out](https://cloud.earthly.dev/login).**

In today's digital age, data is one of the most valuable assets for individuals and organizations alike. Losing data can have a significant impact on productivity, financial stability, and even an organization's reputation. This is why it is crucial to have a reliable and secure method of backing up your data.

Enter Restic, a backup software that facilitates data protection. With its fast, efficient, and secure technology, Restic is the solution you need to protect your valuable data from potential threats.

In this article, you will learn how to configure the Restic backup system on your Unix machine to AWS [S3](/blog/aws-lambda-golang), restore the data, and create a cron job to back up your data automatically.

Let's get started!

## What Is Restic?

Restic is an open-source backup software designed to help individuals and organizations protect their data against potential threats. Restic is written in [Golang](/blog/top-3-resources-to-learn-golang-in-2021) and uses [encryption](/blog/encrypting-data-with-ssh-keys-and-golang) and compression to secure the data and supports multiple platforms, including Windows, MacOS, and Linux. The software can back up data to various storage solutions, such as local drives, remote servers, and cloud services. With its fast, efficient, and secure technology, Restic is a valuable tool for protecting important data and ensuring that it can be recovered in the event of data loss.

## Prerequisites

To follow along with this step-by-step tutorial, you should have the following:

An [AWS account](https://aws.amazon.com/)
Local installation of [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). You should have [configured the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
A Unix Machine: This tutorial uses a Mac Machine

## Creating an Amazon S3 Bucket

As a first step, you need to create an S3 bucket that will be used for your back-up and recovery backend and the required permission to access the bucket. To do so, run the following command

~~~{.bash caption=">_"}
aws s3api create-bucket \
    --bucket back-up-restic \
    --region eu-west-1 \
    --create-bucket-configuration LocationConstraint=eu-west-1

~~~

<div class="wide">
![Creating S3 Bucket]({{site.images}}{{page.slug}}/ED9AIJ2.png)
</div>

You can confirm the created S3 bucket at `https://s3.console.aws.amazon.com/s3/buckets?region=eu-west-1`

<div class="wide">
![Created Bucket]({{site.images}}{{page.slug}}/Ozdl1H8.png)
</div>

<div class="notice--info">
📑 If you receive a bucket name error message, please rename the bucket to a unique name. There is a global namespace for Amazon S3. (In other words, no two S3 buckets can have the same name.) It works similarly to how DNS works in that each domain name must be unique. As a result, when creating S3 buckets, you must use a unique bucket name.
</div>

## Creating a User with Required Access to S3 Bucket

After creating the back-up and recovery S3 bucket, let's create an IAM user and attach the required policy to allow access to the bucket.

Firstly, create a file and name it `restic-policy.json` and paste the following config into it:

~~~{.json caption="restic-policy.json"}
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:PutObject",
          "s3:ListBucket",
          "s3:GetObject",
          "s3:DeleteObject"
        ],
        "Effect": "Allow",
        "Resource": [
          "arn:aws:s3:::back-up-restic",
          "arn:aws:s3:::back-up-restic/*"
        ]
      }
    ]
  }

~~~

This is a policy in AWS that defines the permissions for accessing the S3 bucket named "back-up-restic". The policy specifies that certain actions can be taken on both the bucket itself and the objects within the bucket. The actions that are allowed include:

* "s3:PutObject": This allows for putting or uploading an object to the bucket.
* "s3:ListBucket": This allows for listing the objects in the bucket.
* "s3:GetObject": This allows for getting or downloading an object from the bucket.
* "s3:DeleteObject": This allows for deleting an object from the bucket.

The policy specifies that these actions are allowed with an "Effect" of "Allow". The "Resource" specifies that these actions can be taken on the bucket itself ("arn:aws:s3:::back-up-restic") and on any object within the bucket ("arn:aws:s3:::back-up-restic/*").

Next, you will create an IAM user named `Restic-user` and attach the restic policy you defined in the restic json file to it. To do so, run the following commands:

~~~{.bash caption=">_"}
aws iam create-user --user-name restic-user && aws iam put-user-policy \
--user-name restic-user --policy-name restic-policy --policy-document \
file://restic-policy.json
~~~

This command creates an IAM user with the name "restic-user". The "&&" operator allows you to chain commands together. So after creating the user, the command attaches a policy to the user with the name "restic-policy". The policy document is stored in a local file called "restic-policy.json", and the "aws iam put-user-policy" command is used to attach the policy to the user.

<div class="notice--info">
Make sure that `file://restic-policy.json` is set to the location of the json file you created earlier.
</div>

<div class="wide">
![Created User]({{site.images}}{{page.slug}}/IHXhrlc.jpeg)
</div>

A Restic IAM user has been created and policy attached. Next, you need to create the programmatic access key. Restic will use this key to assume the user's identity. To do so, run the following command:

~~~{.bash caption=">_"}
aws iam create-access-key --user-name restic-user
~~~

<div class="wide">
![Creating Programmatic access key]({{site.images}}{{page.slug}}/GgyBNPw.jpeg)
</div>

Store the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in a safe place, as we'll use them in the next steps.

## Installing Restic

Restic stores data in the encrypted repository, and whenever you add data to the repository, Restic can automatically create a new snapshot. But before taking advantage of the Restic backup utility, you'll first have to install Restic on your machine.

Here's how you can install Restic on the most common UNIX systems.

On a Mac:

~~~{.bash caption=">_"}
brew install restic
~~~

On Debian/Ubuntu:

~~~{.bash caption=">_"}
apt-get install restic
~~~

On Arch Linux:

~~~{.bash caption=">_"}
pacman -s restic
~~~

On Fedora:

~~~{.bash caption=">_"}
dnf install restic
~~~

You now have Restic installed on your machine; you can verify the installation with the `restic version`  command.

## Setting Restic Configuration

![Configure]({{site.images}}{{page.slug}}/configure.png)\

Restic protects your data by encrypting it. This way even if somebody gains access to your S3 bucket, they still cannot read your data. Generate a strong 24+ character password using [LastPass's password generator](https://www.lastpass.com/features/password-generator) or a secure password generator of your choice. Store a copy of this password in a secure location because, without it, your backups will be useless.

After generating your password, using your favorite text editor, create a file named `.restic.env` in your home directory. Inside this file, you are going to add lines for each of the 4 required environment variables. Use the example block below, replacing the values with your own.

~~~{.bash caption=">_"}
export AWS_ACCESS_KEY_ID="AAKIATRM7RJKUY76FNKWH"
export AWS_SECRET_ACCESS_KEY="QCdDl40TWc279gkspCvCStmT9i92wdcyxMXY4/v+"
export RESTIC_PASSWORD="E1bjRCy*CdnU&45Q^l3"
export RESTIC_REPOSITORY="s3:s3.eu-west-1.amazonaws.com/back-up-restic"
~~~

This file contains sensitive data that needs to be protected from other users with `chmod` permissions set to read-only:

~~~{.bash caption=">_"}
 chmod 400 ~/.restic.env
~~~

Next, you need to activate these environment variables in your current bash session:

~~~{.bash caption=">_"}
source ~/.restic.env
~~~

Using this method, your shell credentials will only be active when you need them, rather than being readily available. To confirm that the credentials are set please run the following command:

~~~{.bash caption=">_"}
echo $RESTIC_REPOSITORY
~~~

<div class="wide">
![Configured Environment Variable]({{site.images}}{{page.slug}}/vUtPlMc.png)
</div>

## Initializing Your Repository

Having configured the Restic credentials for accessing your S3 bucket, the next step is to set up a new repository. With Restic, backup data is stored in the initialized repository, and each backup action creates a new snapshot. In this case, the repository is this S3 bucket you created. To initialize this repository, run the following command:

~~~{.bash caption=">_"}
restic init
~~~

<div class="wide">
![Successfully Initialized Bucket]({{site.images}}{{page.slug}}/NVRcKHB.png)
</div>

To confirm the initialization process, on your browser, go to `https://s3.console.aws.amazon.com/s3/buckets/back-up-restic?region=eu-west-1`.

<div class="wide">
![Initialized Repository]({{site.images}}{{page.slug}}/qObdQQ.png)
</div>

Restic initialization configuration has been generated in the S3 bucket, but you can also verify the repository on the command line. To do so run the following commands:

~~~{.bash caption=">_"}
restic check
~~~

<div class="wide">
![Restic Check]({{site.images}}{{page.slug}}/6oCsbGm.png)
</div>

## Backing Up Data to S3 Bucket

![Backup]({{site.images}}{{page.slug}}/backup.png)\

Following the successful initialization of the repository, you can start backing up data to S3. To begin, you will create a file that will be backed up to S3:

~~~{.bash caption=">_"}
# create directory ~/backup-file

mkdir backup-file

# Switch to the ~/backup-file

cd backup-file
~~~

Now create `first-backup.txt` in the backup-file/ directory, with your preferred editor and add the following:

~~~{ caption="first-backup.txt"}
MARY'S LAMB.

Mary had a little lamb,
   Its fleece was white as snow.
And everywhere that Mary went,
   The lamb was sure to go.
He followed her to school one day,
   That was against the rule.
It made the children laugh and play
   To see a lamb at school.

And so the teacher turned him out,
   But still he lingered near,
And waited patiently about
   Till Mary did appear.
And then he ran to her, and laid
   His head upon her arm,
As if he said 'I'm not afraid,
   You'll keep me from all harm.'

'What makes the lamb love Mary so?'
   The eager children smile.
'Oh, Mary loves the lamb, you know,'
   The teacher did reply.
'And you each gentle animal
   In confidence may bind,
And make them follow at your call,
   If you are always kind.'

~~~

Having created the backup-file, the next step is to back it up to S3:

~~~{.bash caption=">_"}
restic backup first-backup.txt
~~~

<div class="wide">
![successfully back-up]({{site.images}}{{page.slug}}/6oCsbGmm.png)
</div>

Next run the following command to list the snapshot taken:

~~~{.bash caption=">_"}
restic snapshots
~~~

<div class="wide">
![Available Restic Snapshot ]({{site.images}}{{page.slug}}/jBAWefU.png)
</div>

Restic, as you can see, took a snapshot of the first backup file and backed it up to S3. However, in real-world scenarios, you will not be backing up a simple text file, but rather system data and configurations, so you will now be backing up your system configuration file at the etc(et-see) directory that stores the configuration on unix systems. To do so, run the following command:

~~~{.bash caption=">_"}
restic backup /etc
~~~

<div class="wide">
![Restic Back-Up]({{site.images}}{{page.slug}}/pOfhWXO.png)
</div>

You can verify the snapshot by running the following command:

~~~{.bash caption=">_"}
restic snapshots
~~~

<div class="wide">
![ Restic Snapshot List ]({{site.images}}{{page.slug}}/zSl1tuV.png)
</div>

Here you created a file and backed it up with Restic, as well as backing up your system etc directory containing your system configuration.

In the next section, you'll learn how to restore data from the S3 bucket.

## Restoring Data From S3 Bucket

Backups aren't complete without their ability to restore files. In the previous section, you backed up the file. Now, let's delete the first backup file from your machine and restore it from the S3 bucket.

Firstly, in the ~/backup-file directory, run the following command to delete the first-backup.txt file:

~~~{.bash caption=">_"}
# delete the firstbackup.txt file 
rm -r first-backup.txt

# ls the content of the directory 
ls
~~~

<div class="wide">
![Deleted File]({{site.images}}{{page.slug}}/QpZzIe7.png)  
</div>

After deleting the text file, the next step is to restore it. Firstly, you should get the id of the text file snapshot. To do so run the following command:

~~~{.bash caption=">_"}
restic snapshots
~~~

<div class="wide">
![Snapshot ID]({{site.images}}{{page.slug}}/UBbALfF.jpeg)
</div>

After getting the snapshot ID the next step is to restore the deleted file by running the following command:

~~~{.bash caption=">_"}
# restore the snapshot with (76a6c637) to the ~/backup-file
restic restore 76a6c637 --target ~/backup-file

# list the contents of the directory 

ls
~~~

<div class="wide">
![Restored and verifying restore snapshot]({{site.images}}{{page.slug}}/fGRMVpV.png)
</div>

## Backing Up Data Automatically with Restic and Cron

At this point, you've already learned all the basic usage of the Restic backup tool. But since manually backing up data can be a pain, why not automatically backup data on your Unix system? Restic, together with Cron, can do wonders, such as automating data backup process. In this section, you will set up a cron job to backup every minute. First, make a file that specifies the location of the directories we want to backup.

In the current directory ~/backup-file, create a file named restic.files, and add the following configurations into it:

~~~{.bash caption=">_"}
/etc
/tmp
/usr
~~~

This file contains the path to all of the directories you want to backup. The same command-line method that you used earlier will work, but you will find it easier to work with a file as the directory you want to back up expands.

Next, you'll set up a cron job to backup the specified directory in the 'restic.files' text file every one minute. Run the [crontab](https://www.computerhope.com/unix/ucrontab.htm) command below to create a new cron job.

~~~{.bash caption=">_"}
crontab -e
~~~

This will open up a file in vim for you. This file is essentially where you can list out your cron jobs — each job on its own line. Once you're on the vim screen, hit A to put the editor into INSERT mode, paste the following cron job configuration:

~~~{.bash caption=">_"}
*/1 * * * * . ~/.restic.env ; /usr/local/bin/restic \
backup --files-from=/Users/mac/backup-file/restic.files \
--tag automated 2>> ~/backup-file/restic.err >> ~/backup-file/restic.log
~~~

This is a cron expression for scheduling a task (using cron) to run the restic backup program every minute (*/1* ** *). It starts by loading [environment variables](/blog/bash-variables) from the file ~/.restic.env using the . (dot) command. Then it runs the restic backup command with the following options:

* `--files-from` specifies the file containing the list of files to be backed up. Change this to the location of the restic.files you created earlier
* `--tag` adds a tag "automated" to the backup.
* The 2>> and >> redirect the standard error and standard output respectively to files in the ~/backup-file directory.

<div class="wide">
![Vim Crontab editor]({{site.images}}{{page.slug}}/I9Akgdx.png)
</div>

Make sure you change the`--files-from=/Users/mac/backup-file/restic.files` to the location of the restic file you created.

After typing out the cron expression, hit `esc` and then type `:wq` to save and exit vim. After exiting the vim editor. Wait a minute and then confirm that crontab is working. To do so run the following command:

~~~{.bash caption=">_"}
restic snapshots
~~~

<div class="wide">
![Automated Restic Back-Up Cron job]({{site.images}}{{page.slug}}/gAMTvtM.png)
</div>

Now that you've created an automated backup system with Restic, you can run the following command to see how much S3 storage you're using:

~~~{.bash caption=">_"}
restic stats
~~~

<div class="wide">
![Restic Storage stat]({{site.images}}{{page.slug}}/DnwyVWY.png)
</div>

To sum up, using Restic, you have set-up a back-up and recovery system that is automated using cron jobs set to run every minute, and ensuring that backups are performed regularly.

## Conclusion

In this guide, you've learned how to use Restic to back up your data, thereby safeguarding it from various risks like natural disasters, cyber attacks, human error, or hardware failures. From setting up an S3 bucket and installing Restic, to initializing a repository, backing up and restoring data, and even automating backups with a cron job, you're now equipped with the skills to effectively protect your data.

Now that you've got backups handled, why not consider boosting your build automation game? If you're interested in further optimizing your tech stack, give [Earthly](https://cloud.earthly.dev/login) a try!

Time to start backing up and building more efficiently!

{% include_html cta/bottom-cta.html %}
