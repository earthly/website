---
title: "Property-Based Testing In Go"
categories:
  - Tutorials
author: Adam

internal-links:
 - just an example
excerpt: |
    Learn how to use property-based testing in Go to automatically generate unit tests and ensure the reliability of your code. Property-based testing is a powerful technique that generates specific test cases based on the properties you want to test, making it easier to catch bugs and ensure the correctness of your code.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about property-based testing in Go. Property-based testing is a powerful technique that can help ensure the reliability and correctness of your code. [Check us out](/).**

Have you ever wanted your unit tests written for you? Property based testing is a powerful testing technique that, in a sense, is just that. You describe the properties you'd like to test, and the specific cases are generated for you.

Property-based testing can be a bit trickier to learn, and not every problem can be well tested in this manner, but it's a powerful technique that's well supported by the go std-lib (`testing/quick`) and that is under-utilized.

## Testing `csvquote`

`csvquote` is a small program that makes it easier to deal with CSV files at the command line. It does this by replacing problematic CSV characters with the controls characters `\x1e` and `\x1f` and later removing them.

You can use it like this:

``` bash
csvquote | head |  csvquote -u
```

I want to improve it a bit, but first, I want to add some testing to ensure I don't break it. The tests will also help me document how it works.

Here are my initial test cases:

``` go
var tests = []struct {
 in  string
 out string
}{
 {`"a","b"`, `"a","b"`},               // Simple
 {"\"a,\",\"b\"", "\"a\x1f\",\"b\""},  //Comma
 {"\"a\n\",\"b\"", "\"a\x1e\",\"b\""}, //New Line
}
```

To test that the `in` string always results in the `out`, I do the following:

``` go
func TestSubstitute(t *testing.T) {
 f := substituteNonprintingChars(',', '"', '\n')
 for _, tt := range tests {
  out := string([]byte(apply([]byte(tt.in), f)))
  assert.Equal(t, tt.out, out, "input and output should match")
 }
}
```

`substituteNonprintingChars` returns a function that does the conversion and `apply` is a helper for applying that function over a `[]byte`.

Slightly simplified, it looks like this:

``` go
func apply(data []byte, f mapper) []byte {
 count := len(data)

 for i := 0; i < count; i++ {
  data[i] = f(data[i])
 }
 return data
}
```

The second thing I want to test is that I can reverse this operation. That is, when `csvquote` is run with `-u`, it should always return the original input.

I can test this by going in reverse from output to input:

``` go
func TestRestore(t *testing.T) {
 f := restoreOriginalChars(',', '\n')
 for _, tt := range tests {
  in := string([]byte(apply([]byte(tt.out), f)))
  assert.Equal(t, tt.in, in, "input and output should match")
 }
}
```

`restoreOriginalChars` is the function that restores the string to its original form.

Both these tests pass (the full source is [on GitHub](https://github.com/adamgordonbell/csvquote/blob/7f4698ad3d3c2d12f063b5d8a8bd304e8307a089/cmd/cvsquote/main_test.go)). However, it's still possible there are edge cases that work incorrectly. What I need is a way to generate more test cases.

## Property-Based Testing

One way I could improve my testing is to combine the two tests. That is, rather than testing that the substituted value matches expectations and that the restored value matches expectations, I can simply test that substituting and restoring a string always results in the original string.

That is for almost all possible values of the string `a`:

``` bash
echo a | csvquote | csvquote -u == a
```

In my go test, I can state that property like this:

``` go
func doesIdentityHold(in string) bool {
 substitute := substituteNonprintingChars(',', '"', '\n')
 restore := restoreOriginalChars(',', '\n')
 substituted := apply([]byte(in), substitute)
 restored := string([]byte(apply(substituted, restore)))
 return in == restored
}
```

That is, for a string `in`, substituting and then restoring it should equal itself. I'm calling this `doesIdentityHold` because an identity is any function that returns the original result. `csvquote | csvquote -u` should be an identity.

### Quick Check

Now that we have that function, we can use `testing/quick`, the property-based testing library, to test it:

``` go
func TestIdentity1(t *testing.T) {
 if err := quick.Check(doesIdentityHold, nil); err != nil {
  t.Error(err)
 }
}
```

By default, this will cause `testing/quick` to run 100 iterations of my identity test, using random strings as inputs. You can bump that up much higher, like so:

``` go
func TestIdentity1(t *testing.T) {
 c := quick.Config{MaxCount: 1000000} // <- changed
  if err := quick.Check(doesIdentityHold, &c); err != nil {
  t.Error(err)
 }
}

```

And with that number of tests cases, I run into a problem:

``` bash