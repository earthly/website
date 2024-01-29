---
title: "Put Your Best Title Here"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "thoughts"
internal-links:
 - just an example
---
*Following from  (Rust, Ruby, and the Art of Implicit Returns")[/single-expression-functions]*

Here is some Java. The Java I learned in university was Java 1.something and the concepts behind Java were simple. "In Java, everything is a object" I was told. I mean, you had classes and abstract classes and interfaces but really objects were what we were supposed to focus on. So you'd do smoething like this a lot:

```
interface Greeter {
    void greet();
}

public class HelloWorld {
    public static void main(String[] args) {
        Greeter greeter = new Greeter() {
            @Override
            public void greet() {
                System.out.println("Hello, world!");
            }
        };
        greeter.greet(); // Outputs: Hello, world!
    }
}
```

I wrote a lot of Java Swing at the time. So I felt like Java was a lot about writing Anonymous Inner Class like this:
```
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        JOptionPane.showMessageDialog(frame, "Button was clicked!"));
    }
});

```

Now Java has lambdas, so I assume I could now write:

```
button.addActionListener(e -> JOptionPane.showMessageDialog(frame, "Button was clicked!"));
```

And my greeter could be something like:
```

Greeter greeter = () -> System.out.println("Hello, world!");
```

This is so much nicer. Less boilerplate to write and less place for bugs to hide. I feel the same way about if expressions.

```
if( x > 7){
  y = 5
} elseif (x > 5) {
  y = 4
} else {
  y' = 3
}
```


```
y = if( x > 7){
  5
} elseif (x > 5) {
  4 
} else {
  3
}
```

There are some redudancies in the first, and because of that its possible to have errors. The boilerplate parts of code, you do learn to skim over, but those parts can have bugs and hence the error in the first version. The slightly shorter expression based code has less room for error.

## Cognitive Downsides

There is a cost, though. These concepts add complexity and make learning the language harder. First I was taught 'In Java everything is an object' and then 'In Java, everything is an object, except primitive types' and then we have to add some footnote that a lambda is just syntax for a object with one method and we keep adding on little exceptions or wrinkles. Even when all the concepts fit together really nicely, there is still just strictly more to learn.

But, its worth it. Learning is a cost that you just pay once and in return you get a more expressive langauge. Beginner readablity suffers, but really the readablity that matters is the readabiltiy of a experienced langauge user and removing repetitive boilerplate improves that.

I'm not a C++ programmer, but C++'s `constexpr` seems like another great example:
```
constexpr double circleArea(double radius) {
    return 3.14159 * radius * radius;
}

constexpr double area = circleArea(5.0); 
```

But if syntaxitical sugar and more language features are a net win for experience uses why did Java succeed so much when it was quite simple and why is Go gaining in popularity today?

There are probably lots of factors. But when it comes to language features their are two obvisous ones. One is the steep learning curve.


## Too Clever By Half

I may be able to show you each language feature of a language in isolation and how it makes things better. But this isn't how they get used in practice. In practice, experts in a lanaguage, use all the language features together. And to an outsider this can be quite confusing. 

In an expressive enough langauge, it reminds me to the 'Focused' in 'A Deepness In The Sky':

> Reynolt cut the audio. “They went on like this for many days. Most of it is a private jargon, the sort of things a close-bound Focused pair often invents.”
>
> Nau straightened in his chair. “If they can only talk to each other, we have no access. Did you lose them?”
>
> “No. At least not in the usual way."

The book is excellent and in it groups of experts obsessed with a problem, can spin off into an internal language no outside can make sense of. They may come up with powerful results, but its inscruatble to the outside. 

And this is what sort of what happens when a developer most familar with Java 8, inherits a Scala program that does a relatively simple task and opens its up to find its written in some sort of functional effect system. 

```
def program: Effect[Unit] = for {
  h <- StateT[Effect1, Requests, String]((requests: Requests) => 
    ReaderT[Effect0, Config, (Requests, String)]((config: Config) => 
      EitherT(Task.delay(
        ((requests, host.run(config))).right[Error]
      ))))
  p <- StateT[Effect1, Requests, Int]((requests: Requests) => 
    ReaderT[Effect0, Config, (Requests, Int)]((config: Config) => 
      EitherT(Task.delay(
        ((requests, port.run(config))).right[Error]
      ))))
  _ <- println(s"Using weather service at http://\$h:\$p\n")
    .liftM[ErrorEither]
    .liftM[ConfigReader]
    .liftM[RequestsState]
  _ <- askFetchJudge.forever
} yield ()
```
( from Pawel Szulc excellent talk: https://www.youtube.com/watch?v=y_QHSDOVJM8 )


This example is a little over the top, but the reaction is a real thing that happens when someone first encounters code from a language using complex syntax, advanced concepts and concise code all at once. 

This isn't just a Fp thing either. Let's compare this go code:
```
func maximumCount(nums []int) int {
    var pos, neg int = 0, 0
    for _, e := range nums {
        if e > 0 {
            pos++
        } else if e < 0 {
            neg++
        }
    }

    if pos > neg {
        return pos
    } else {
        return neg
    }
}
```
https://www.youtube.com/watch?v=U6I-Kwj-AvY


With a C++ solution:
```
int maximumCount(vector<int>& nums) {
    return std::max(
        std::ranges::count_if(nums, [](auto e) { return e > 0; }),
        std::ranges::count_if(nums, [](auto e) { return e < 0; })
    );
}

```
Or a Rust solution
```
pub fn maximum_count(nums: Vec<i32>) -> i32 {
    let pos = nums.clone().into_iter().filter(|e| *e > 0).count() as i32;
    let neg = nums.into_iter().filter(|e| *e < 0).count() as i32;
    std::cmp::max(pos, neg)
}
```

The thing I want to get across is that this Scala, C++ and Rust code all may cause a certain reaction if you are unfamilair with the constructs in use, but actually are quite different. 

All maximum count versions use the constructs of the language to express the algorithm in a nice way, that requires familarity with the concepts at hand. They are an expressiveness win. 

The Scala solution is actually where complaints can come. It's cleverness masterbation. It's a simple problem, expressed in a complex way, either to show off or to entertain, to keep things interesting for the developer.




```
def maximumCount(nums: Array[Int]): Int =
  max(nums.count(_ < 0),(nums.count(_ > 0)))
```


## But its complex
Here why this is all confusing. If you know all the intricate features of a langauge, then of course given a solution you might reach for solving it using those things. And it might not be apparent that that makes new-comers struggle, it s just the obvious way to structure the solution. It's just the curse of knowledge. 

And also most people in expressive languages are interested in using the features at hand. And if you learn about a new feature, or library or technique or whatever, you might want to use it. And maybe sometimes you use it when its not strictly needed. 

But use some constraint. Everybody with a new tool goes through a maxmilist phase where they end up using something more than they should and pushing a concept to its limits. But maybe do that in a side project and not the thing someone else is going to inherit.

If you're in a group, and you've developed a house style to solving problem that might be great. But if a new person joins, who is bright and earger and you struggle to get them up to speed, that could be a good chance to think about why that is the case.


## The Other Side

The other sidde of this is tricky as well. If you encounter code or even al whole programming langauge where the code seems too clever by half, I think, just my personal opinion, that you can't actually make that call yet. 

Until you know the idioms of the languge, and the way its various features work and interact its very hard to tell how to judge a given solution. Maybe what you are looking at is an idea that is very well encapsulated in the expressiveness of the languauge. A solution with just ifs and elses would be so verbose as to be difficult to hold in your head, while using chunkier building blocks the idea is clear.  

But perhaps the complex code is the opposite. Maybe if shakespeare had made a cookbook would write them as sonnets or iambic pentameter. But that wouldn't make the reciepts turn out any better. That would just be someone bored, trying to make the work more interesting for themselves at the expenses of future readers.


## Conclusion: I don't know

So, yeah, new syntax, and programming language features can make code denser. That can improve readability for those familar with the langauge. 

It's also a new tool people can write horrible code in. Is that worse then people writing horible code with other simpler constructus? It might be, but its hard to judge a solution if you don't know the langauge.  The thing you think is werid might just be foreigh. If you're going to spend your career doing this, it makes sense to keep learning. To use lanaguge that allow experts to cleanly solve problems. 

On the whole, I think expressivity is a win but yeah, dont leave cleverness masterbation piles of code for others to inherit. Then you are just going to give a bad name to the language you presumably like. If you're bored, start side project and go wild.  
