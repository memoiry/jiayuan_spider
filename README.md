# jiayuan_spider


A multi-thread spider to pick up all users' pictures in [世纪佳缘](http://www.jiayuan.com/)

## Usage

There are there parameters you need to provide.

1. User name
2. Password
3. Order, which is used to split the whole task into different order for multi-computer downloading. Since the whole data is huge, I have split the task into 160 order. So you can choose set order from [1-160]. It's roughly estimated that there is 43000000 users and nearly 100000000 photos.
4. Optional: thread, you can choose how many thread you wish to use for the spider. Default is 30.

**Resuming from broken downloads is supported since the probability of the website banning your IP address is high once your downloading speed is too aggressive. So, once your IP address is banned, simply change your IP and run the command again.**

### Example

```bash
$ python jy_spider.py --user memoiry --password memoiry --order 20 --thread 30
```


<p align="center"><img src="https://i.loli.net/2017/08/20/5999abeb5220e.png" width=500></img></p>

So it could crawl 5 people persecond in my computer.

Have fun!




