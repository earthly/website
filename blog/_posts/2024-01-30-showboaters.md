---
title: "Showboaters, Maxmialists and You"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "thoughts"
---
*Following from [Rust, Ruby, and the Art of Implicit Returns](/single-expression-functions)*

The Java I learned in university was Java 1.X, and the concepts were simple. "In Java, everything is an object," I was told. I mean, you had classes and abstract classes and interfaces, but really, objects were what we were supposed to focus on.

So you'd do something like this a lot:

~~~{.java caption="Inner Class Java"}
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
~~~

I wrote a lot of Java Swing at the time. So I felt like Java was a lot about writing Anonymous Inner Class like this:

~~~{.java caption="Old Fashioned Java Swing"}
button.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
        JOptionPane.showMessageDialog(frame, "Button was clicked!"));
    }
});

~~~

Now Java has lambdas, so I assume I could now write:

~~~{.java caption="Java with Lambda"}
button.addActionListener(e -> 
  JOptionPane.showMessageDialog(frame, "Button was clicked!"));
~~~

And my greeter could be something like:

~~~{.java caption="More Java with Lambda"}

Greeter greeter = () -> System.out.println("Hello, world!");
~~~

This is so much nicer. Less boilerplate to write and fewer places for bugs to hide. I feel the same way about if expressions.

~~~{.scala caption="If"}
if( x > 7){
  y = 5
} elseif (x > 5) {
  y = 4
} else {
  y' = 3
}
~~~

~~~{.scala caption="If expression"}
y = if( x > 7){
  5
} elseif (x > 5) {
  4 
} else {
  3
}
~~~

There are some redundancies in the first, and because of that, it's possible to have errors. You do learn to skim over the boilerplate parts of code, but those parts can have bugs, hence the error in the first version. The slightly shorter expression-based code has less room for error.

I'm not a C++ programmer, but C++'s `constexpr` seems like another great example. Doing things at compile time previously involved templates, but now you can use `constexpr`:

~~~{.cpp caption="constexpr in c++"}
constexpr double circleArea(double radius) {
    return 3.14159 * radius * radius;
}

constexpr double area = circleArea(5.0); 
~~~

But if syntactical sugar and more language features are a net win for experienced users, why did Java succeed so much when it was quite simple? Why is Go succeeding? Why was there skepticism when Swift came out? Why do I know many people with an aversion to C++ or Scala?

There are lots of factors. One is a steep learning curve, but another is the showboaters.

## Learning Curve

Expressivity has a cost. These concepts add complexity and make learning the language harder.

<div class="align-left">
 {% picture grid {{site.pimages}}{{page.slug}}/9850.png --picture --img width="260px" --alt {{ Learning Curve }} %}
</div>

First, I was taught 'In Java, everything is an object' and then 'In Java, everything is an object, except primitive types', and then we had to add some footnote that lambda is just syntax for an object with one method that is made on the fly. And so on, we keep adding on little exceptions or wrinkles. Even when all the concepts fit together nicely, there is still just strictly more for a newcomer to learn.

But it's worth it. Learning is a cost that you just pay once, and in return, you get a more expressive language. Beginner readability suffers, but really, the readability that matters is the readability of an experienced language user, and removing repetitive boilerplate improves that.

However, complexity can compound.

## Compounding Complexity

I may be able to show you each language feature of a language in isolation and how it makes things better. But this isn't how they get used in practice. In practice, experts use all the language features together. And to an outsider, this can be quite confusing.

In an expressive enough language and with a group of strong developers, you can end up with something like the 'Focused' in 'A Deepness In The Sky':

> Reynolt cut the audio. "They went on like this for many days. Most of it is a private jargon, the sort of things a close-bound Focused pair often invents."
>
> Nau straightened in his chair. "If they can only talk to each other, we have no access. Did you lose them?"
>
> "No. At least not in the usual way."

The book is excellent, and without saying too much, in it, groups of experts obsessed with a problem can spin off into an internal jargon no outsider can make sense of. In the worst case, they may come up with powerful answers to important questions, but the whole thing is inscrutable to the outsider.

And this is sort of what happens when a developer most familiar with Java 8 inherits a Scala program that does a relatively simple task and opens it up to find it written in some sort of functional effect system.

~~~{.scala caption="Call a service in an Effect Stack in Scala"}
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
~~~

( from Pawel Szulc excellent talk: <https://www.youtube.com/watch?v=y_QHSDOVJM8> )

This example is a little over the top, but the reaction is a real thing that happens when someone first encounters code from a language using complex syntax, advanced concepts, and concise code all at once.

This isn't just an FP thing, either. Let's compare this go code:

~~~{.go caption="Count Max"}
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
~~~

<https://www.youtube.com/watch?v=U6I-Kwj-AvY>

With a C++ solution:

~~~{.cpp caption="Count Max C++"}
int maximumCount(vector<int>& nums) {
    return std::max(
        std::ranges::count_if(nums, [](auto e) { return e > 0; }),
        std::ranges::count_if(nums, [](auto e) { return e < 0; })
    );
}

~~~

Or a Rust solution

~~~{.cpp caption="Count Max Rust"}
pub fn maximum_count(nums: Vec<i32>) -> i32 {
    let pos = nums.clone().into_iter().filter(|e| *e > 0).count() as i32;
    let neg = nums.into_iter().filter(|e| *e < 0).count() as i32;
    std::cmp::max(pos, neg)
}
~~~

This Scala, C++, and Rust code may all cause a certain reaction in the unfamiliar. But the examples are actually quite different. One is showboating, and one is not.

## Crafting Clarity

All maximum count versions use the constructs of the language to express the algorithm in a nice way. They require familiarity with the concepts at hand, but they are an expressiveness win.

~~~{.j caption="J"}
MaximumCount =. 0&(<./.>.) (+//)
~~~

<figcaption>This J solution uses dyadic operators yet is clear and direct to those who know J (or so I've been told)</figcaption>

The Scala solution is actually where complaints can come. In almost all cases, if you are inheriting code like that – code that reads a host and a port for a weather service and then gets the forecast for your city - if you inherit code like that, and it's not in the context of research chaining effects - then someone is showboating. It's a simple problem expressed in a complex way. Maybe to show off or maybe for self-entertainment. Sometimes, people make things complex to keep themselves interested.

It can be hard to impute reasons behind a solution without all the context.

## Pure Show Boating Is Rare

~~~{.go caption="Showboating goroutines"}
func main() {
    numbers := []int{1, 2, 3}

    sumChan := make(chan int)
    go func() {
        sum := 0
        for _, num := range numbers {
            sum += num
        }
        sumChan <- sum
    }()

    totalSum := <-sumChan
    fmt.Printf("Total Sum: %d\n", totalSum)
}
~~~

I think pure showboating is rare and rarely totally intentional. If you know all the intricate features of a language, then, of course, when you create a solution for a problem, you might reach for those features. And it might not be apparent that this will make newcomers struggle; it s just the obvious way to structure the solution. It's just the curse of knowledge.

And add to that the fact that most people using an expressive language are enjoying the power they wield. And if you learn about a new feature, library or, technique, or whatever, you might want to use it. And maybe sometimes you use it when it's not strictly needed. And you wake up one day, and no one outside your group understands your code.

So use some constraint. Everybody goes through a maximalist phase where they end up using some feature more than they should and pushing a concept to its limits. But maybe do that in a side project and not the thing someone else is going to inherit.

~~~{.csharp caption="RayTracer in Single Statement"}
...
from y in Enumerable.Range(0, screenHeight)
  let recenterY = -(y - (screenHeight / 2.0)) / (2.0 * screenHeight)
  select from x in Enumerable.Range(0, screenWidth)
    let recenterX = (x - (screenWidth / 2.0)) / (2.0 * screenWidth)
    let point = ...
    let ray = // And so on for 60 lines
...
~~~

<figcaption>This in [LINQ Ray Tracer](https://github.com/lukehoban/LINQ-raytracer) is cool, but nobody wants to inherit it.</figcaption>

If you're in a group, and you've developed a house style for solving problems, that might be great. But if a new person joins who is bright and eager, and you struggle to get them up to speed, that could be a good chance to think about why that is the case.

## Give It A Chance

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/0240.png --picture --img width="300px" --alt {{ Rub Goldberg Code }} %}
</div>

The other side of this is tricky as well. If you encounter code or even a whole programming language where the code seems too clever by half, I think you should hold your opinion for a bit.

Until you know the idioms in use and the way various features work and interact, it's hard to tell how to judge a given solution. Maybe that foreign-looking solution is actually very well encapsulated in the expressiveness of the language in a way that is just unfamiliar. Maybe a solution with just ifs and loops would be so verbose as to be difficult to hold in your head all at once.

Maybe not, though. Some people are just looking for challenges and will create them where none exists. But... if you don't know the idioms and patterns of the language, it might be too early to make that call.

Programming language features can make code clearer. They can improve readability. Each feature is also a new tool people can use to write horrible code in. Is that worse than people writing horrible code with other simpler constructs? It might be, but it's hard to judge a solution if you don't know the language.

If you're going to spend your career doing this, it makes sense to keep learning. To use a language that allows experts to cleanly solve problems. But yeah, just don't leave piles of esoteric code around for others to inherit.
