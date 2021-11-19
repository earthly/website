---
title: "Property Based Testing In Go"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

## Draft.dev Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`

* Intro

Have you ever wanted your unit tests written for you? Property based testing is a powerful testing techinque that in a sense is just that. You describe the properties you'd like to test and the specific cases are generated for you.

It's a powerful techique that is underused. In this article I'll go over a specific example of using property based testing.

* Testing CSVQuote

CSVquote is a program that makes it easier to deal with CSV files at the command line. It does this by replacing problematic CSV characters with controls characters `\x1e` and `\x1f` and then later removing them. I'd like to make some changes to it, but first I want to add some testing to make sure I don't break it ( and to document how it works ).

Here are my test cases:

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
		out := string([]byte(substitute([]byte(tt.in), f)))
		assert.Equal(t, tt.out, out, "input and output should match")
	}
}
```

The second thing I want to test is that I can reverse this operation. When `csvquote` is run with `-u` it should always return the original input.

I can test this by going in reverse from output to input:

``` go
func TestRestore(t *testing.T) {
	f := restoreOriginalChars(',', '\n')
	for _, tt := range tests {
		in := string([]byte(substitute([]byte(tt.out), f)))
		assert.Equal(t, tt.in, in, "input and output should match")
	}
}
```

Both these tests pass (the full source is [here]()). However, it's still possible there are edge cases that work incorrectly. What I need is a way to generate more test cases.

## Property Based Testing

One way I could improve my testing, is to combine the together the two tests. That is, rather than testing that the substituted value matches some result and that the unrestored value matches some result we can simple test that substituting and restoring a string always results in the original string.

That is for almost all possible strings s [^1]:

``` bash
echo s | csvquote | csvquote -u == s
```

In my go test, I could state that like this:
``` go
func identityTest(a string) bool {
	convert := substituteNonprintingChars(',', '"', '\n')
	restore := restoreOriginalChars(',', '\n')
	c := substitute([]byte(a), convert)
	b := string([]byte(substitute(c, restore)))
	return b == a
}

```
That is, a string `a`, converted and unconverted equals itself. I'm calling this `indentityTest` because an identity is any function that returns the original result. `csvquote | csvquote -u` should be an identity. 

### Quick Check

Now that we have that function, we can use `testing/quick`, the quick check library, to test it.

```
func TestIdentity1(t *testing.T) {
	if err := quick.Check(idTest, nil); err != nil {
		t.Error(err)
	}
}
```

By default, this will cause quickcheck to run 100 iterations of our identity test, using random strings as inputs. We can bump that up much higher just to get a through test:

```
func TestIdentity1(t *testing.T) {
	c := quick.Config{MaxCount: 1000000} // <- changed
  if err := quick.Check(idTest, &c); err != nil {
		t.Error(err)
	}
}

```
And with that number of tests cases it eventually finds a problem:
``` bash
--- FAIL: TestIdentity1 (5.17s)
    main_test.go:43: #13072: failed on input "\x1f\U00037f8b\U000732a1\"
FAIL
```

But what I've actually found is a problem in my test. You see `csvquote` should always be able to reverse it's input except in the case that the input contains the non-printable ASCII control characters `csvquote` uses to do its magic. 

`\x1f` may not be used much outside of traditional teletype terminals but I asked quickcheck to check across all possible strings, and eventually it found a failing case.

Long term, it probably makes sense to have `csvquote` exit with an error condition if it receives input it can't handle but that is a problem for another day. Instead let's focus on constraining the input used in the tests.


## Writing a Property Testing Generator

As I've shownm `testing/quick` can generate test values for testing on its own, but now I need to write my own.

This allows me to make a couple improvements to the test. I can remove control characters from the test set, but also I can generate strings that are valid CSV files, since my main concern is that `csvquote` can handle valid csv files, not the entire universe of strings. Testing random strings might find some exciting edge cases, but there is a much larger chance of finding an error when we send in valid CSV input.

First I write a function to generate random strings of size `size` and from the characture set `alphabet`:

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

Then I used that to generate CSV rows 
``` go
func RandCSV(r *rand.Rand) string {
	var sb strings.Builder
	lines := r.Intn(20) + 1
	rows := r.Intn(20) + 1
	for i := 0; i < lines; i++ {
		for j := 0; j < rows; j++ {
			if j != 0 {
				sb.WriteString(`,`)
			}
			sb.WriteString(fmt.Sprintf(`"%s"`, RandCSVString(r)))
		}
		sb.WriteString("\n")
	}
	return sb.String()
}

func RandCSVString(r *rand.Rand) string {
	s := RandString(r, 20, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01233456789,\"")
	return strings.Replace(s, `"`, `""`, -1) // In CSV all double quotes must be doubled up
}

```
Which look like this:
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
``` 
func TestIdentity2(t *testing.T) {
	c := quick.Config{MaxCount: 10000,
		Values: func(values []reflect.Value, r *rand.Rand) {
			values[0] = reflect.ValueOf(RandCSV(r))
		}}
	if err := quick.Check(idTest, &c); err != nil {
		t.Error(err)
	}
}

```
And now I can test `csvquote` against ten thousand random CSV files in under a second each test run. 

``` bash
> go test
PASS
ok      github.com/adamgordonbell/csvquote/cmd/cvsquote 0.635s
```

I'll leave extending to cover unicode values and unquoted rows for another day.

### Property Testing 

Property based testing is a powerful techique for testing your code. As you can see from this somewhat contrived scenario it moves the work of testing away from specific test cases and towards general cases that hold for all possible inputs. Here the property under test was that substituting and restoring are reversible operations (and form an identity).

The hardest part of property based testing, espeically intially, is seeing what properties should be tested for. It's not always immediately clear what's possible to test in this manor and some tests are simply hard to state generically. But when a problem is well suited for property based testing it is a powerful tool.

( The second hardest thing about property based testing is writing generators for your problem domain. Although once written they make testing in this style feel quite natural. )