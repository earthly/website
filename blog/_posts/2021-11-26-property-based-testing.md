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
**We're [Earthly](https://earthly.dev/). We simplify and speed up software building through containerization. If you're into property-based testing, you care about reliability and then Earthly is a great fit. [Give us a try](/)!**

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
--- FAIL: TestIdentity1 (5.17s)
    main_test.go:43: #13072: failed on input "\x1f\U00037f8b\U000732a1\"
FAIL
```

The failing test is helpfully printed. However, it's found a problem in my testing method, not with the code under test. You see, `csvquote` should always be able to reverse it's input, *except in the case that the input contains the non-printable ASCII control characters* and that is what this test case has found.

`\x1f` may not be used much outside of traditional teletype terminals but I asked `csvquote` to check across all possible strings, and eventually, it found a failing case.

Long term, I should adjust `csvquote` to exit with an error condition when it receives input it can't handle, but that is a problem for another day. Instead let's focus on constraining the input used in the tests.

## Writing a Property Testing Generator

As I've shown above, `testing/quick` can generate test values for testing on its own, but it's often valuable to write your own.

In this case, writing my own CSV file generator will allow me to make a couple of improvements to the test. First of all, I can remove control characters from the test set. But also, I can move to generating strings that are valid CSV files, rather than just random characters. Testing with random characters is easy, but my main concern is that `csvquote` can handle valid CSV files, so by narrowing in on that case, I'll have a better chance of catching real-world issues.

First I write a function to generate random strings of size `size` and from the character set `alphabet`:

``` go
func RandString(r *rand.Rand, size int, alphabet string) string {
 var buffer bytes.Buffer
 for i := 0; i < size; i++ {
  index := r.Intn(len(alphabet))
  buffer.WriteString(string(alphabet[index]))
 }
 return buffer.String()
}
```

It outputs what I expect:

``` go
r := rand.Rand{}
println(RandString(&r, 5, "abc"))
println(RandString(&r, 5, "abc"))
```

```
caccb
cabbb
```

Then I used that to generate a CSV files with random number or lines and rows:

``` go
func randCSV(r *rand.Rand) string {
 var sb strings.Builder
 lines := r.Intn(20) + 1
 rows := r.Intn(20) + 1
 for i := 0; i < lines; i++ {
  for j := 0; j < rows; j++ {
   if j != 0 {
    sb.WriteString(`,`)
   }
   sb.WriteString(fmt.Sprintf(`"%s"`, randCSVString(r)))
  }
  sb.WriteString("\n")
 }
 return sb.String()
}

func randCSVString(r *rand.Rand) string {
 s := RandString(r, 20, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01233456789,\"")
 return strings.Replace(s, `"`, `""`, -1) // In CSV all double quotes must be doubled up
}

```

Here is what calling `randCSVString` will generate:

``` ini
"7IWvdDEGTxlRdJZrc4Ra","LMHcCcN,D2RVRsfbw0IF",",LrZ3B4SvFEfG3FqO01n","""vY4FmzhbyR4iDgYpr6f","sw83uJkitIc8trzaYmEO"
"fGloXshqwC""O9Bd,eM,L","LDRajiwNgZNitCA0QL11","1Q
nqhMhzu7Mlu92qxK""8","jtj33vTlH5VP4UlbKu2e","sDhVlor4RRg4JrKfdR""W"
"EGWYmpm1TVNdB3rfmU80","Mx0RdqqVUuWiOpKY""IXk","ctprb8
7PrVu8rX8iJqTg","wnmagEjUDJrZCGBdmAYH","EJtuq1ZJqz9jf,j6vzh1"
",88Q7qWLewZVK9pE83ut","1kZJipoz2FOWLS96xMjW","5BkVvtZqZk""S2wpOB3rQ","kYN6aGPDmgSLAEI4CJtu","xOH,9y9wDDtwWUPsjgz7"
"mbexX2,Wl4""cuq3VGekP","uMXK5uLDz2ZS3Wv4wynY","KJBLt0RipsJyEqVHqrDx","glDHHs6Ujyg""piJGv595","rIa4KOxe,B""qS7EmO
nTB"
```

I can then hook this up to my test method:

``` go
func TestIdentity2(t *testing.T) {
 c := quick.Config{MaxCount: 10000,
  Values: func(values []reflect.Value, r *rand.Rand) {
   values[0] = reflect.ValueOf(randCSV(r))
  }}
 if err := quick.Check(doesIdentityHold, &c); err != nil {
  t.Error(err)
 }
}

```

And now I can test `csvquote` against ten thousand random CSV files in under a second.

``` bash
> go test
PASS
ok      github.com/adamgordonbell/csvquote/cmd/cvsquote 0.635s
```

I'll leave extending this to covering Unicode values and unquoted rows for another day.

### Property Testing

Property-based testing is a powerful technique for testing your code. As you can see from this real-world but somewhat contrived scenario, it moves the work of testing away from specific test cases and towards validating properties that hold for all values. Here the property under test was that substituting and restoring are inverses of each other (and therefore form an identity).

For me, the most challenging part of property-based testing is seeing how I can transform a specific test-case into a testable property. It's not always immediately clear what's possible to test in this manner and some tests are simply hard to state in this form. But when a problem is well suited for property-based testing, it is a powerful tool!

( The second most challenging thing about property-based testing is writing generators for your problem domain. Although once written, they make testing in this style feel quite natural. )

## More Resources

The hardest part of this style of testing is seeing where and how it can apply. The places I've found it valuable include:

- Verifying serialization and deserialization code
- Verifying an optimization (by comparing the results to the un-optimized version)
- Anywhere I have more than one representation of some data and need to test the boundaries of those representations.

But others have found more ways to use this paradigm. If you want to learn more about property-based testing, then [`gopter`](https://github.com/leanovate/gopter), *the GOlang Property TestER*, is worth taking a look at. [Amir Saeid](https://github.com/amir), who's good at this technique, recommends this [book](https://leanpub.com/property-based-testing-in-a-screencast-editor) full of examples, and [this blog](https://jacobstanley.io/how-to-use-hedgehog-to-test-a-real-world-large-scale-stateful-app/).

If you have any tips or suggested resources for property-based testing, please let me know on Twitter (<a href="https://twitter.com/adamgordonbell/">@adamgordonbell</a>).

And if you care about reliable software, take a look at Earthly. Earthly makes continuous integration less flakey and works with your existing workflow.

{% include_html cta/bottom-cta.html %}
