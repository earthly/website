---
title: "Rust Concurrency Patterns for Parallel Programming"
categories:
  - Tutorials
toc: true
author: Ikeh Akinyemi
editor: Mustapha Ahmad Ayodeji

internal-links:
 - patterns for parallel programming
 - rust concurrency patterns
 - concurrency patterns
 - parallel programming
excerpt: |
    This article explores Rust's concurrency features and provides an overview of basic concurrency primitives such as threads, shared ownership, and message passing. It also covers more advanced topics like error handling, performance optimization, testing, parallel programming with Rayon, and asynchronous programming with Tokio.
last_modified_at: 2023-08-28
---
**Rust concurrency presents challenges. This article covers some patterns to overcome them. Earthly reliably reproduces builds for Rust applications with complex dependencies. [Check it out](/).**

Rust is a modern programming language that prioritizes performance, safety, and concurrency. It's a unique language thanks to its memory safety guarantees, ownership, and borrowing system, and support for [fearless concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html).

Concurrency gives programs the capability to execute multiple tasks simultaneously, enabling enhanced efficiency and responsiveness. It allows programs to take full advantage of modern hardware with multiple cores and processors.

In this guide, developers who are new to Rust will learn all about concurrency and how to use it. This article assumes you have basic programming knowledge but are new to Rust and its unique features.  

## Why Rust Excels at Concurrency

Rust is an ideal language for writing concurrent programs because it was designed with concurrency in mind. Rust's ownership and borrowing system ensures safe and efficient memory management, preventing [data races](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/nomicon/races.html) and other concurrency bugs. This system allows developers to write concurrent code with confidence, knowing that the compiler catches many common errors before they become bugs.

## Threads in Rust

![Threads]({{site.images}}{{page.slug}}/threads.png)\

One of the most basic primitives for concurrency in Rust is threads. A thread is an independent path of execution within a program that can run concurrently with other threads.

Threads allow developers to take full advantage of multicore processors by dividing a task into smaller subtasks that can be executed in parallel.

Now that you know what threads are, let's explore how threads are created and joined in Rust.

### Creating and Joining Threads

To create a new thread in Rust, you can use the [`std::thread::spawn`](https://doc.rust-lang.org/std/thread/fn.spawn.html) function, which requires a closure as its argument. This closure contains the code that executes in the new thread.

For example, you can use the following code to create a new thread:

~~~{.rust caption="main.rs"}
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        // code to be executed in the new thread
    });
}
~~~

In the above snippet, you imported the `thread` module with the statement use std::thread;. In the main function, you utilize the `thread::spawn` function to create a new thread. This function returns a [`JoinHandle`](https://doc.rust-lang.org/std/thread/struct.JoinHandle.html) type, which represents the new thread. You can utilize the `JoinHandle` type to synchronize and wait for the thread to complete its execution. This is achieved by invoking the `join` method on the `Joinhandle` like this:

~~~{.rust caption="main.rs"}
use std::thread;

fn main() {
    let handle = thread::spawn(|| {
        // code to be executed in the new thread
    });
    
    match handle.join() {
        Ok(result) => {
            // handle success case with result
        },
        Err(_) => {
            // handle error case
        }
    };
}
~~~

Here, the function call to the `join` method returns a `Result<T>` type. The `match` expression handles the `Result`. If the variant of `Result` is `Ok`, the result value is accessed and used to handle the success case; however, if the variant is `Err`, then the error is handled within the error code block.

### Sharing Data Between Threads

For multiple threads to work together, they need to be able to share data. Rust provides several ways to share data between threads, including shared [ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html) and message passing.

#### Shared Ownership

One way to share data between threads is to use shared ownership with the [`Arc`](https://doc.rust-lang.org/std/sync/struct.Arc.html) (Atomically Reference Counted) smart pointer. An `Arc` allows multiple threads to share ownership of a value, making sure the value is not dropped until all threads are finished using it:

~~~{.rust caption="main.rs"}
use std::sync::Arc;
use std::thread;

fn main() {
    let shared_data = Arc::new(42);

    let handle = thread::spawn({
        let shared_data = shared_data.clone();

        move || {
            // use the shared_data value in the new thread
        }
    });

    // do some work in the main thread...

    let result = match handle.join() {
        Ok(result) => {
            // handle success case with result
        },
        Err(_) => {
            // handle error case
        }
    };
}
~~~

In this code, you imported an `Arc` struct that facilitates the sharing of the value`42` between the primary thread and the newly spawned thread. In the primary thread (*i.e.* the `main()` function), you created an instance of the `Arc` struct, then created the new thread using the `thread::spawn` function. Within the new thread, you used the `Arc`'s [`clone`](https://doc.rust-lang.org/std/sync/struct.Arc.html#impl-Clone-for-Arc%3CT%3E) method to generate a new reference to the shared data, 42. This reference is subsequently passed on to the new thread.

After this, the primary thread (the main execution thread of the program) continues to perform some tasks. It then joins with the newly spawned thread using the `handle.join()` method. This will either return the result of the new thread, if it finished successfully, or handle an error case, as appropriate. This process signifies the culmination of the primary thread's work in relation to the new thread.

#### Message Passing

Another way to share data between threads is to use message passing with [channels](https://doc.rust-lang.org/rust-by-example/std_misc/channels.html). Channels allow threads to send messages to each other, which can be used to share data and coordinate tasks.

For instance, in the following example, a message is passed using two threads: a primary thread and a spawned thread. In this example, the primary thread sends data through a channel, and the spawned thread receives the data through the same channel:

~~~{.rust caption="main.rs"}
use std::sync::mpsc;
use std::thread;

fn main() {
    let (sender, receiver) = mpsc::channel();

    let handle = thread::spawn(move || {
        match receiver.recv() {
            Ok(data) => {
                // use the data value in the new thread
            }
            Err(err) => {
                // handle the error
            }
        }
    });

    // do some work in the main thread

    let data = 42;
    match sender.send(data) {
        Ok(()) => {}
        Err(_) => {
            // handle error
        }
    };
}
~~~

In this snippet, the line `use std::sync::mpsc;` imports the [`mpsc`](https://doc.rust-lang.org/std/sync/mpsc/struct.SyncSender.html) module from Rust's standard library. `mpsc` stands for "multiple producers, single consumer". This module provides functionality for synchronizing data between threads, including channels for message passing. In the next line, you import the `thread` module.

Within the `main` function, the line `let (sender, receiver) = mpsc::channel();` creates a new channel. The `channel` function from the `mpsc` module returns a tuple containing two values: a sender and a receiver. And as the names indicate, the sender sends data into the channel, and the receiver receives data from the channel. The `let` keyword destructures this tuple and assigns the sender and receiver to separate variables.

Next, the `let handle = thread::spawn(move || {...})` line spawns a new thread. The `thread::spawn` function takes a closure (a function literal) as an argument and runs this closure in a new thread. Before the closure, the `move` keyword transfers ownership of captured variables (in this case, the `receiver`) to the new thread.

Inside the spawned thread, `match receiver.recv() {...}` receives a message from the channel. On the `receiver,` the [`recv()` method](https://doc.rust-lang.org/std/sync/mpsc/struct.Receiver.html#method.recv), which is a blocking method, waits for a message to be sent to the channel. If a message is received, it returns `Ok(data)`, and if an error occurs (*e.g.* if the sender has been dropped and no further messages can be sent), it returns `Err(err)`. The `match` keyword can handle both of these outcomes.

Back in the primary thread, `let data = 42; match sender.send(data) {...}` sends a message (*ie* `42`) to the channel. The [`send()`](https://doc.rust-lang.org/std/sync/mpsc/struct.Sender.html#method.send) method on the `sender` sends a value into the channel. If the send is successful, it returns `Ok(())`, and if an error occurs (*e.g.,* if the receiver has been dropped and no further messages can be received), it returns `Err(_)`. Again, the `match` keyword is used to handle these two possible outcomes.

### Managing Thread Synchronization

To prevent data races and other concurrency bugs that may arise when multiple threads access shared data, Rust offers various [thread synchronization primitives](https://doc.rust-lang.org/book/ch16-03-shared-state.html), such as locks, mutexes, and atomic variables, which you'll learn about in the following sections.

## Concurrency Patterns

![Patterns]({{site.images}}{{page.slug}}/patterns.png)\

Concurrency patterns are reusable solutions to common problems that occur in concurrent programming. In Rust, several patterns are available, and the following sections will discuss three of them: mutexes and locks, channels, and atomic reference counting.

### Mutexes and Locks

A mutex, derived from the term *mutual exclusion*, serves as a synchronization mechanism that permits exclusive access to a shared resource by a single thread at any given time. Its purpose is to prevent data races, which occur when multiple threads concurrently access the same memory location with at least one of them modifying it.

To create a mutex in Rust, you need to use the `Mutex` type from the `std::sync` module. For example, the following example shows you how to use the mutex to wrap shared data, ensuring only one thread can modify it at a time:

~~~{.rust caption="main.rs"}
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut val = counter.lock().unwrap();
            *val += 1; 
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
~~~

In this example, you create a mutex called `counter` and wrap it in an `Arc`. Then you spawn ten threads using `thread::spawn`, each of which increments the value of the `counter`.

To modify the `counter`'s value, each thread must acquire the lock by calling `counter.lock().unwrap()`. If another thread has already acquired the lock, the calling thread blocks until the lock is released. Once the lock is acquired, the thread increments the `counter`'s value by dereferencing the mutex value and adding one to it.

### Channels

A channel serves as a conduit through which data can be sent as a means of communication and synchronization between concurrent threads. It ensures that data is sent and received safely and efficiently.

In the following example, you'll see how channels can be used to coordinate tasks with deadlines in a concurrent setting:

Import the necessary modules:

~~~{.rust caption="main.rs"}
use std::sync::mpsc;
use std::thread;
use std::time::{Duration, Instant};
~~~

This code imports the necessary modules for multi-threading, creating channels, and time-related operations.

Define the worker function:

~~~{.rust caption="main.rs"}
fn worker(receiver: mpsc::Receiver<Instant>) {
    loop {
        let deadline = match receiver.recv() {
            Ok(deadline) => deadline,
            Err(_) => break,
        };

        let now = Instant::now();
        if now >= deadline {
            println!("Worker received a task after the deadline!");
        } else {
            let remaining_time = deadline - now;
            println!("Worker received a task. Deadline in {:?}.", \
            remaining_time);
            thread::sleep(remaining_time);
            println!("Task completed!");
        }
    }
}
~~~

In this snippet, you have a `worker` function that receives deadlines through a channel (`mpsc::Receiver`) and processes the tasks accordingly. Each task is associated with a deadline represented by an `Instant` value.

Inside the `loop`, the function attempts to receive a message from the channel using `receiver.recv()`. This is a blocking operation that waits until a message is available. Then using the match expression, you handle the received value; if `Ok(deadline)` is returned, it means a task with a deadline has been received. The `deadline` value is extracted and stored. But If `Err(_)` is returned, it indicates an error occurred, and the loop is broken, terminating the worker thread.

 Next, the current time is obtained using `Instant::now()` and stored in the `now` variable.

The code then checks whether the current time (`now`) has exceeded the received task's deadline (`deadline`). If the deadline has passed, it prints a message indicating that the worker received the task after the deadline.

If the deadline has not passed, the remaining time until the deadline is calculated by subtracting `now` from `deadline`, and the result is stored in the `remaining_time` variable.

A message is printed indicating that the worker received the task and the remaining time until the deadline.

The worker thread then sleeps for the duration of the `remaining_time` using `thread::sleep(remaining_time)`. This pauses the execution of the worker thread, simulating work being performed for the specified duration.

After the sleep, a message is printed indicating that the task has been completed.

The worker function continues to loop, waiting for new tasks to be received through the channel. If an error occurs during the receiving operation, such as the channel being closed, the loop is broken, and the worker thread terminates.

Define the `main` function:

~~~{.rust caption="main.rs"}
fn main() {
    let (sender, receiver) = mpsc::channel();

    let worker_handle = thread::spawn(move || {
        worker(receiver);
    });

    // Sending tasks with different deadlines
    sender.send(Instant::now() + Duration::from_secs(3)).unwrap();
    sender.send(Instant::now() + Duration::from_secs(5)).unwrap();
    sender.send(Instant::now() + Duration::from_secs(7)).unwrap();
    sender.send(Instant::now() + Duration::from_secs(4)).unwrap();

    // Signal no more tasks and wait for the worker to finish
    drop(sender);
    worker_handle.join().unwrap();
}
~~~

In the `main` function, you create a channel (`mpsc::channel`) for communication between the main thread and the worker thread. Then you spawn the worker thread, passing in the receiver end of the channel.

Next, you send several tasks with different deadlines to the worker by calling `sender.send`. The worker receives these tasks from the channel and processes them accordingly. After sending all the tasks, you can signal no more tasks by dropping the sender end of the channel. This informs the worker that no further tasks will be arriving. Then you wait for the worker thread to finish using `worker_handle.join().unwrap()`.

Now let's run the code and see the output:

~~~{ caption="Output"}
Worker received a task. Deadline in 2.999960875s.
Task completed!
Worker received a task. Deadline in 1.994807292s.
Task completed!
Worker received a task. Deadline in 1.994865667s.
Task completed!
Worker received a task after the deadline!
~~~

The usage of channels in the above snippets demonstrates a common pattern in concurrent programming, where multiple threads can communicate by sending messages through a shared channel, ensuring synchronized and orderly execution/communication.

### Arc

An `Arc` is a smart pointer that provides shared ownership of a value across multiple threads. It uses [atomic operations](https://doc.rust-lang.org/std/sync/atomic/) and [reference counting](https://doc.rust-lang.org/std/rc/) to efficiently track the number of references to the shared data. This allows multiple threads to access and modify the shared data concurrently.

For instance, let's simulate a scenario where you might have three files, and you want to read all of them at the same time—concurrently, using multiple threads. After you read the files, you collect their contents into a shared data structure (*i.e.,* a shared vector). The code is documented inline:

Import the required module:

~~~{.rust caption="main.rs"}
use std::sync::{Arc, Mutex};
use std::fs::File;
use std::io::{self, BufRead};
use std::thread;
~~~

This code imports the required modules for multi-threading, file operations, I/O, and synchronization.

Define the `main` function:

~~~{.rust caption="main.rs"}
fn main() {
    // File paths to read
    let file_paths = vec!["file1.txt", "file2.txt", "file3.txt"];
    let shared_data = Arc::new(Mutex::new(Vec::new()));

    let mut handles = vec![];

    // Spawn threads to read files concurrently
    for file_path in file_paths {
        let shared_data = Arc::clone(&shared_data);
        let handle = thread::spawn(move || {
            // Open the file
            let file = File::open(file_path).expect("Failed to open file");

            // Read the contents of the file
            let lines: Vec<String> = io::BufReader::new(file)
                .lines()
                .map(|line| line.expect("Failed to read line"))
                .collect();

            // Lock the shared data
            let mut data = shared_data.lock().unwrap();

            // Append the lines to the shared data
            data.extend(lines);
        });

        handles.push(handle);
    }

    // Wait for all threads to finish
    for handle in handles {
        handle.join().unwrap();
    }

    print!("{:#?}", shared_data.lock().unwrap());

    // Explicitly drop the Arc
    drop(shared_data);

    // Attempting to access the shared data after dropping /
    // the Arc would result in a compile-time error
    // Uncomment the following line to see the error:
    // let data = shared_data.lock().unwrap();
}
~~~

In this snippet, a vector of file paths and a `shared_data` variable of type `Arc<Mutex<Vec<String>>>` is created. Then you spawn three threads to read each file simultaneously. For each file path, a new `Arc` reference is created, allowing each thread to possess its reference to the shared data, ensuring safe concurrent access.

Within each thread's execution, the file is opened, and its contents are read line by line, storing them in a vector of strings.

To access the shared data, the thread locks the associated mutex using the [`lock()` method](https://doc.rust-lang.org/std/sync/struct.Mutex.html#method.lock), guaranteeing exclusive access to the shared vector.

The lines read from the file are then appended to the shared vector using the [`extend()` method](https://doc.rust-lang.org/std/iter/trait.Extend.html#method.extend), modifying the shared data in a synchronized manner. Once a thread finishes processing a file, it releases the lock, enabling other threads to access the shared data concurrently. The main thread waits for all the spawned threads to complete execution by utilizing the `join()` method.

Finally, the `Arc` reference is explicitly dropped using the [`drop()` function](https://doc.rust-lang.org/std/mem/fn.drop.html), which deallocates the `Arc` and its associated data. Afterward, any attempt to access the shared data will result in a compile-time error, preventing any further use of the shared data.

Before executing this code, make sure to create the three text files named "file1.txt", "file2.txt", and "file3.txt" in the same directory where the Rust program is located. You can use a text editor or any other method to create these files. Make sure to add the following content to the files:

Filename: `./file1.txt`:

~~~{ caption="file1.txt"}
Get a sneak peak of your memory
Pragmatism policy
~~~

Filename: `./file2.txt`:

~~~{ caption="file2.txt"}
Big team big win
~~~

Filename: `./file3.txt`:

~~~{ caption="file3.txt"}
Set deliverable 
before 
you burnout.
~~~

Now let's run the code and see the output:

~~~{ caption="Output"}
[
    "Set deliverable ",
    "before ",
    "you burnout.",
    "Get a sneak peak of your memory",
    "Pragmatism policy",
    "Big team big win",
]
~~~

In this example, `Arc` is used to ensure safe concurrent access to the shared vector `shared_data`. By cloning the `Arc` using `Arc::clone`, each thread obtains its own reference to the shared data. The reference counting mechanism of `Arc` ensures that the shared data is deallocated only when all references are dropped, allowing multiple threads to safely read and modify the shared vector.

## Concepts Related to Concurrency Patterns

![Concepts]({{site.images}}{{page.slug}}/concept.png)\

There are also other concepts related to concurrent programming that provide insights into effective strategies and techniques for writing robust and efficient concurrent Rust code. In the following sections, you'll learn about concepts such as error handling in concurrent code, balancing performance and readability, testing concurrent code, parallel programming with [Rayon](https://github.com/rayon-rs/rayon), and async programming using the [Tokio](https://tokio.rs/) library.

### Error Handling in Concurrent Code

Rust's error-handling mechanism is designed to be expressive, concise, and safe. In concurrent code, Rust provides various ways to handle errors, such as using `Result` types, `match` statements, and error propagation.

In previous code blocks, you've utilized error handling, but in the following example, you'll focus on the constructs used for error handling, specifically in the context of threading and message passing:

~~~{.rust caption="main.rs"}
use std::thread;
use std::sync::mpsc::channel;

fn main() {
    let (tx, rx) = channel();
    …
~~~

The code above imports `thread` and `channel`, which are necessary modules from the standard library. The `channel()` function creates the sender and receiver ends of the channel, which are destructured and assigned to the variables `tx` and `rx`, respectively. Next, it's time to spawn a thread:

~~~{.rust caption="main.rs"}
    …
    let handle = thread::spawn(move || {
        // Perform some computation...
        let result = 42;
    …
~~~

Here, you spawn a thread and perform some computations (represented here with the assignment of the value `42` to `result`) in the thread that you spawned. Then, you send the computed result over the channel using `tx.send(result)`:

~~~{.rust caption="main.rs"}
    …
        // Send the result over the channel
        let send_result = tx.send(result);
        match send_result {
            Ok(_) => Ok(()),
            Err(e) => Err(e),
        }
    });
    …
~~~

The `send` method returns a `Result` type which is stored in `send_result`. If the sending was successful, `Ok(())` is returned. Otherwise, the error is returned with `Err(e)`.

Then, you need to use the `handle.join().unwrap()` function to wait for the spawned thread to finish:

~~~{.rust caption="main.rs"}
        …
    // Wait for the thread to finish and handle any errors that occur
    let thread_result = handle.join().unwrap(); 
    // Note: unwrap is safe here because we are propagating any \
    // errors through the Result type
        …
~~~

The `unwrap()` method extracts the `Ok` variant value from the `Result` returned by `handle.join()`. If the `Result` is `Err`, `unwrap()` will panic and crash the program. This is safe in this context because the error from the `Result` type is propagated:

~~~{.rust caption="main.rs"}
    …
    match thread_result {
        Ok(_) => {
            // Receive the result from the channel
            let result = rx.recv();
            match result {
                Ok(val) => println!("Result: {}", val),
                Err(e) => println!("Error receiving result: {:?}", e),
            }
        },
        Err(e) => println!("Error sending result: {:?}", e),
    }
}
~~~

A `match` statement handles the `thread_result`. If it's `Ok`, the main thread attempts to receive the result from the channel using `rx.recv()`, which also returns a `Result` type. If receiving the value is successful, it prints the result. If it encounters an error, it prints the error.

As you can see, Rust has a robust error-handling mechanism, allowing for safe and effective error handling in concurrent programming scenarios. By using the `Result` type and `match` expressions, errors can be concisely captured and handled, ensuring the reliability of the program.

### Balancing Performance and Readability

Concurrent programs can be challenging to write because they often require careful consideration of performance trade-offs. Rust provides a variety of tools for optimizing performance, such as low-level concurrency primitives (*i.e.,* threads, mutexes, and atomic variables) and unsafe code. Unsafe code in Rust refers to sections of code that are explicitly marked as [`unsafe`](https://doc.rust-lang.org/std/keyword.unsafe.html), signifying that the compiler can't guarantee the usual safety guarantees, often because it involves operations like raw pointer dereferencing or [calling functions written in other languages](https://doc.rust-lang.org/nomicon/ffi.html). However, these tools come at the cost of reduced safety and increased complexity like deadlocks, race conditions, or undefined behavior if used incorrectly.

It's important to balance performance considerations with the readability and maintainability of your code. One way to do this is to use high-level concurrency abstractions, such as [Crossbeam](https://docs.rs/crossbeam/latest/crossbeam/), Rayon, and Tokio, wherever possible and only resort to low-level primitives when necessary. These abstractions offer convenient APIs that abstract away low-level implementation details, eliminating the need for extensive knowledge in those areas.

### Testing Concurrent Code

When testing concurrent code in Rust, it's important to ensure that your tests are deterministic and do not suffer from race conditions or deadlocks. You can achieve this by using Rust's built-in testing framework and implementing your tests with proper synchronization mechanisms.

One approach is to use a mutex to ensure that the test is run in a thread-safe manner. You can also use a [`Condvar`](https://doc.rust-lang.org/stable/std/sync/struct.Condvar.html) to allow threads to wait for a signal from another thread. A Condvar, or "condition variable", is a synchronization primitive in Rust that can be used to block threads until a certain condition is met.

Let's write a multi-threading test involving three threads trying to increase a shared resource. In the following code, you write a function that checks if it's the thread's turn to access/increment the shared resource. If it's not, it waits on the condition variable for a certain condition to be met and notifies you when the condition might be met, making the threads work together in a synchronized manner:

~~~{.rust caption="main.rs"}
use std::sync::{Arc, Mutex, Condvar};
use std::thread;

fn count_to_10(shared_data: Arc<(Mutex<u32>, Condvar)>, thread_num: u32) {
    let &(ref mutex, ref cvar) = &*shared_data;
    let mut count = mutex.lock().unwrap();

    while *count < 10 {
        if *count % 3 == thread_num {
            *count += 1;
            cvar.notify_all();
        } else {
            count = cvar.wait(count).unwrap();
        }
    }
}
~~~

Here you define a `count_to_10` function, which takes two parameters: `shared_data`, an `Arc` containing a tuple of a `Mutex` and a `Condvar`, and `thread_num`, an identifier for the current thread. This function represents the logic for each thread to count up to 10.

First, you destructure the `shared_data` tuple into references to the `Mutex` and `Condvar` using the `&*` syntax. This will allow you to conveniently access the mutex and condvar later.

Next, you acquire a lock on the mutex by calling `mutex.lock().unwrap()`. The lock is automatically released when the `count` variable goes out of scope.

Inside the `while` loop, you check if the current value of `count` is less than 10. If it is, you proceed with counting. You determine if it's the current thread's turn to count by checking if `count % 3` is equal to `thread_num`.

If it's the thread's turn to count, you increment the count by 1 and then call `cvar.notify_all()` to notify other threads waiting on the condition variable for the condition to be met.

If it's not the thread's turn to count, you call `cvar.wait(count).unwrap()` to wait on the condition variable until it's signaled by another thread. This releases the lock on the mutex and puts the thread to sleep until it is awakened by a call to `cvar.notify_all()`.

~~~{.rust caption="main.rs"}
#[test]
fn test_count_to_10() {
    let shared_data = Arc::new((Mutex::new(0), Condvar::new()));
    let mut handles = Vec::new();

    for i in 0..3 {
        let shared_data = shared_data.clone();
        let handle = thread::spawn(move || {
            count_to_10(shared_data, i);
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }
}
~~~

In the above snippet, you define a test function `test_count_to_10`. It sets up the shared data, spawns the threads, waits for them to finish, and asserts that the final count is `10`.

First, you create an `Arc` called `shared_data` that contains a tuple with an initial count of 0 (wrapped in a `Mutex`) and a new `Condvar` instance.

Next, you create an empty vector called `handles` to store the thread handles.

Inside the `for` loop, you iterate from 0 to 2 (inclusive) using `i` as the thread number. For each iteration, you clone the `shared_data` to ensure each thread has its own reference to the shared data. Then, you use `thread::spawn` to create a new thread and pass the cloned `shared_data` and the thread number `i` to the `count_to_10` function.

The returned thread handles are collected and stored in the `handles` vector.

Finally, you iterate over the `handles` vector and call `join()` on each handle to wait for the threads to finish.

The `unwrap()` method is used to propagate any potential errors that might occur during thread execution.

Now let's test the code and see the output:

~~~{ caption="Output"}
running 1 test
test test_count_to_10 ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 
0 filtered out; finished in 0.00s
~~~

After the threads finish counting, the test function asserts that the final count is `10`, ensuring that the synchronization was successful.

### Parallel Programming With Rayon

[Rayon](https://github.com/rayon-rs/rayon) is a data parallelism library for Rust that allows you to write parallel and concurrent programs by providing abstractions and utilities that abstract away the complexities of managing threads and their synchronization. It's designed to work with Rust's ownership and borrowing system, and it can automatically manage thread pools to optimize performance.

To use Rayon, you need to add the `rayon` crate to your `Cargo.toml` file:

~~~{.rust caption="main.rs"}
[dependencies]
rayon = "1.7"
~~~

Next, let's explore how to use Rayon to parallelize a merge sort algorithm, which is a divide-and-conquer sorting algorithm that works by recursively splitting an array into halves, sorting those halves, and merging them back together until it reaches the base case with only one element or an empty array:

~~~{.rust caption="main.rs"}

fn merge_sort_par(arr: &mut [i32]) {
    if arr.len() <= 1 {
        return;
    }

    let mid = arr.len() / 2;
    let (left, right) = arr.split_at_mut(mid);

    rayon::join(|| merge_sort_par(left), || merge_sort_par(right));

    //...
}
~~~

The function `merge_sort_par` takes a mutable reference to an array of integers. The first thing it does is check whether the array length is less than or equal to 1. If it is, the function returns because an array with one or zero elements is already sorted.

Next, it calculates the middle index of the array and splits it into two halves at this point. The `split_at_mut(mid)` function returns two mutable slices: one for the left half of the array and one for the right half.

The `rayon::join` function then sorts these two halves in parallel. It takes two closures that it executes concurrently. In this case, each closure is a recursive call to `merge_sort_par` on one half of the array.

~~~{.rust caption="main.rs"}
    //...

    let mut i = 0;
    let mut j = mid;
    let mut temp = Vec::with_capacity(arr.len());

    while i < mid && j < arr.len() {
        if arr[i] < arr[j] {
            temp.push(arr[i]);
            i += 1;
        } else {
            temp.push(arr[j]);
            j += 1;
        }
    }

    while i < mid {
        temp.push(arr[i]);
        i += 1;
    }

    while j < arr.len() {
        temp.push(arr[j]);
        j += 1;
    }

    arr.copy_from_slice(&temp);
}
~~~

Once the two halves are sorted, the function merges them back together in sorted order. It does this by initializing two indices, `i` and `j`, and a temporary vector, `temp`, to hold the sorted array.

It then enters a loop where it compares the elements at the current indices of the two halves. It pushes the smaller element onto `temp` and increments the corresponding index. This continues until all elements from one half have been pushed onto `temp`.

If there are remaining elements in either half (which means one half had fewer elements than the other), it pushes those remaining elements onto `temp`.

Finally, it copies the sorted elements from `temp` back into the original array with the `copy_from_slice` function.

~~~{.rust caption="main.rs"}
fn main() {
    let mut arr = vec![8, 2, 5, 9, 1, 3, 7, 6, 4];
    merge_sort_par(&mut arr);
    println!("{:?}", arr);
}
~~~

In the `main` function, a mutable array `arr` is created and passed to `merge_sort_par` to be sorted. The sorted array is then printed to the console:

~~~{ caption="Output"}
[1, 2, 3, 4, 5, 6, 7, 8, 9]
~~~

This indicates that the array has been sorted in ascending order.

This implementation takes advantage of Rayon's automatic work stealing to parallelize the sorting algorithm efficiently across all available CPU cores.

### Async Programming in Rust

Asynchronous programming is an essential technique for writing high-performance I/O-bound applications. Rust has built-in support for asynchronous programming with the `async`/`await` syntax and the [`futures`](https://docs.rs/futures/latest/futures/) library. In this section, you'll learn how to write asynchronous Rust programs using the [`Tokio`](https://github.com/tokio-rs/tokio) library.

The Tokio library provides an asynchronous runtime that can run multiple tasks concurrently on a single thread or across multiple threads. It also provides a set of utilities and abstractions for writing asynchronous programs, such as futures, streams, and tasks.

To use Tokio, you need to add it as a dependency in your `Cargo.toml` file:

~~~{.rust caption="main.rs"}
[dependencies]
tokio = { version = "1.11.0", features = ["full"] }
~~~

Once you've added it as a dependency, write a simple program that downloads the content of a web page asynchronously using the `request` crate to perform the HTTP request:

~~~{.rust caption="main.rs"}
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut stream = TcpStream::connect("example.com:80").await?;

    let request = "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n";
    stream.write_all(request.as_bytes()).await?;

    let mut response = Vec::new();
    stream.read_to_end(&mut response).await?;

    println!("{}", String::from_utf8_lossy(&response));

    Ok(())
}
~~~

In this example, you use the `tokio::net::TcpStream` type to open a TCP connection to the `example.com` server. Then you send an `HTTP GET` request and read the response asynchronously using the `read_to_end` method before the response is printed in the console.

> **Please note:** You can use the `async`/`await` syntax to write asynchronous code that looks like synchronous code. You can also use `await` to wait for a future to complete before proceeding to the next line of code.

You can also use Tokio to perform parallel computation using `tokio::task::spawn`:

~~~{.rust caption="parallel computing.rs"}
use tokio::task;

#[tokio::main]
async fn main() {
    let handle1 = task::spawn(async {
        // perform some expensive computation asynchronously
    });

    let handle2 = task::spawn(async {
        // perform some other expensive computation asynchronously
    });

    let (result1, result2) = tokio::join!(handle1, handle2);

    // combine the results of the two tasks
}
~~~

In this snippet, you use the `tokio::task::spawn` method to spawn two tasks that perform some expensive computation asynchronously. Then you use the `tokio::join!` macro to wait for both tasks to complete and collect their results.

Tokio also provides a set of abstractions for working with asynchronous streams, such as `tokio::io::AsyncRead` and `tokio::io::AsyncWrite`, and asynchronous channels, such as `tokio::sync::mpsc::channel`. These abstractions can make it easy to write high-performance asynchronous network servers.

## Conclusion

Rust's concurrency features make it a powerful language for writing high-performance, concurrent programs. In addition, Rust's memory safety guarantees, ownership, and borrowing system, and support for fearless concurrency make it a great choice for writing safe and performant concurrent code.

In this article, you learned all about the basics of Rust's concurrency primitives. In addition, you learned about some more advanced concepts, such as error handling, performance optimization, testing, parallel programming, and async programming. The code example used in this tutorial can be found in this [GitHub repository](https://github.com/Ikeh-Akinyemi/earthly-draftdev).

If you're looking to learn more about concurrency patterns, check out the following resources:

* [*Rust by Example*](https://doc.rust-lang.org/rust-by-example/) provides hands-on examples and explanations of Rust concepts.
* [*Asynchronous Programming in Rust*](https://rust-lang.github.io/async-book/02_execution/02_future.html) covers the fundamentals.
* [*Rust Cookbook*](https://rust-lang-nursery.github.io/rust-cookbook/) offers a collection of practical recipes for Rust programming.

{% include_html cta/bottom-cta.html %}
