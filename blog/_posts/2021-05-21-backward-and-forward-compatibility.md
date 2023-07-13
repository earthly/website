---
title: "Protocol Buffers Best Practices for Backward and Forward Compatibility"
categories:
  - Tutorials
toc: true
author: John Gramila
internal-links:
 - protocol buffers
 - backward compatibility
 - backwards compatibility
 - forwards compatibility
topic: go
last_modified_at: 2023-04-17
excerpt: |
    This article explores best practices for maintaining backward and forward compatibility with Protocol Buffers. Learn how to manage your messages and make changes without breaking your system.
---
**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article covers protocol buffers and forward and backward compatibility. If you want to know more about building in containers then [check us out](/).**

Protocol Buffers serialize structured data so it can be efficiently stored or shared over a network. They were designed for internal use at Google in 2001 and released to the public under an open-source license in 2008.

Protocol Buffers are compiled to a series of strictly arranged bytes, so they can be transmitted very efficiently. After reconstitution, they can also be understood by a wide range of languages. Let's examine protobufs first at a high level, then do a deep dive into best practices for working with them to see if they're a fit for your expanding data workflow.

## What Exactly Are Protocol Buffers?

Protocol Buffers are designed with the concept of extensibility at their core. You can add fields without a care, though you do have to be attentive when modifying or removing fields. This article will go through how you can manage your messages to maintain forward and backward compatibility.

Protocol Buffers are most useful when regularly sharing small pieces of data (generally under 1 MB) between two computers on a regular basis. It's designed for extracting and sharing that data, but it's also very effective at storing data that will have to be shared between systems using different languages or controlled by different organizations.

Protocol Buffers are also great at persisting blobs of data, particularly in languages like C++ where you can use protobuf as a data struct. If you're communicating with lots of computers a little at a time, Protocol Buffers will save you network bandwidth.

### Understanding Backward and Forward Compatibility

Both backward and forward compatibility is important for any project you expect will run for a long time. There are at least two parts to any protobuf system, the sender and the receiver. If either one can be upgraded to a new message format, and the system functionality continues uninterrupted then the message protocol is both forward and backward compatible.

<div class="notice notice--big">

#### Backward Compatibility

If a client that was updated to a new message type but is still able to understand the previous message type then the message change is backward compatible. Backward compatibility is being able to understand messages from a previous version.
</div>

<div class="notice notice--big">

#### Forward Compatibility

If a message is changed and a non-updated client can still understand and process the message then the message change is forward compatible. Forward compatibility is being able to understand messages from a future version.
</div>

With Protocol buffers, if a sender is upgraded, the receiver can still understand messages if it is forward compatible. It can accept input crafted by later versions of protobuf. The sender is backward compatible because it's creating output that can be consumed by earlier versions. So long as you're careful about when and how you change and remove fields, your protobuf will be forward and backward compatible.

### Getting Started With Buffers

The first step to making a Protocol Buffer is to define data structures in a `.proto` file. For each data structure you want to create, you'll make a `message` that contains a name and data type for each field it contains.

``` protobuf
syntax = "proto3";
package tutorial;

message Sample{
  string content = 1;
  int32 id = 2;
  string situation = 3;
}
```

These declarations in the `.proto` file are shared with both the message sender and receiver to construct immutable getters and setters that allow data to be read into and accessed from binary using a [compiler](/blog/compiling-containers-dockerfiles-llvm-and-buildkit), then accessed in a variety of programming languages.

## Tips for Maintaining Compatibility

Compatibility starts with defining the syntax and version of protobuf the sender and receiver are using. The `package` makes sure your code is namespaced to avoid any collisions. It is possible to have a sender using `proto3` while a receiver uses `proto2` (or any other combination) as long as you're careful about what fields you include. Both the sender and receiver have strict definitions of existing fields—you can make changes as long as you don't disturb those definitions.

### Create (Numerical) Order

From a compatibility perspective, unique field numbers are the most vital piece of the message declaration. These numbers (the `= 1` after the name declaration) are used as identifiers for fields after they are converted to binary. When the message is decoded, a crucial step for compatibility is allowing the parser to skip fields it doesn't recognize so it's possible to add new fields without breaking programs that weren't designed to look for them.

The unique field number is combined with a wire type corresponding to the data type of the field. This identifier and type combination form the key of every field in a message. These fields combined give the receiver the ability to uniquely identify fields and determine the length of the field, so it knows when to start looking for the next field.

This means once a unique field number or length is set, it cannot be changed. Any program consuming or serializing protobuf data needs the number to be fixed forever, or both the sender and all the receivers must be updated.

Encoding the numbers 1 through 15 takes one byte to encode, 16 through 2047 take two bytes, and so on. In situations where the size of messages is important, the most frequently exchanged data should have the smallest field numbers. The language is designed to effectively handle new fields, but because you can't change the identifier of fields, it may be wise to leave yourself a couple gaps in these high-efficiency identifier ranges in case a very common field pops up in the future.

One of the best ways to prevent problems with overlapping or misunderstood field numbers is to use the `reserved` keyword. If you wanted to remove the `type` field in your `Sample` message, any applications running the protobuf version that contained that field would break if the identifier was removed and then reused for some other field.

To get around these compatibility issues, you can reserve identifiers. You can also reserve ranges of identifiers; here you're reserving a range and the removed value of `1`:

``` protobuf
message Sample{
  reserved 1, 5 to 8;
  int32 id = 2;
  string text = 3;
}
```

### Beware of Required Fields

Another tricky part of compatibility is the required modifier preceding the data type. In the second version of protobuf, there were three modifiers to choose from: `optional`, `repeated`, and `required`. The `required` option was removed in `protobuf3`, because it requires careful planning to ensure compatibility. If a required field is missing from a message, readers will consider the message incomplete and return an error.

Instead, consider writing custom validation or use default values within your application to handle required fields. In `protobuf2`, you were able to set [default values](https://developers.google.com/protocol-buffers/docs/proto#optional "Default fields in protobuf2"), in `protobuf3`, every field type has a [fixed default value](https://developers.google.com/protocol-buffers/docs/proto3#default "Default fields in protobuf3").

### Avoid Groups

Another feature of `protobuf2` that should be avoided to ensure compatibility is Groups. These enable nesting information inside method definitions. A Group combines a nested message type and a field into a single declaration using the `group` keyword.

The recommended way to nest messages is to nest them, then call them:

``` protobuf
message SampleContainer {
message Sample{
  optional int32 id = 2;
  optional string text = 3;
}
   repeated Sample samples = 1;
}
```

The difference between nested message types and Groups is the wire format they use.

### Adding New Fields

New fields can be safely added in any version of protobuf, but there are still compatibility considerations to be aware of. Pay attention to the depreciation of the `required` fields and transition from user-specified defaults to protobuf-specified defaults. The application receiving protobuf data has to be responsible for handling the [default values](https://developers.google.com/protocol-buffers/docs/proto3#default) for any new fields.

You generally can freely change the name and order of fields. However, when you're producing JSON serialized data with protobuf, the field names are also reserved by the receiver. This requires users to reserve **field identifiers and names** when removing or deprecating fields.

### Keep an Eye on Compatibility When Changing Field Types

Because field types are also used to determine when the receiver ends a field, changing field types across versions without carefully checking for compatibility can also cause problems. There are many specific [rules](https://developers.google.com/protocol-buffers/docs/proto3#updating "Rule for updating fields") about how to change field types, but a good standard is to avoid ever changing the wire type of any field. If you're in a situation where you need to change a field type, the best path forward is to deprecate the existing field and put the new information into a new field.

### Don't Destroy, Deprecate

Protocol Buffer compatibility problems generally start when you need to change the length of or remove existing fields. There are a whole host of rules about how fields can [change](https://developers.google.com/protocol-buffers/docs/proto3#updating "Protobuf3 update fields").

Largely, maintaining backward and forward compatibility comes down to maintaining a consistent wire type. You can't change the wire type or alter the length of fields and expect old code to properly send or receive messages—the sender's and receiver's understanding of the exact length of each element in the transmitted messages needs to be precise.

<!-- vale HouseStyle.Spelling = NO -->
|Type|Meaning|Used For|
|--- |--- |--- |
|0|Varint|int32, int64, uint32, uint64, sint32, sint64, bool, enum|
|1|64-bit|fixed64, sfixed64, double|
|2|Length-delimited|string, bytes, embedded messages, packed repeated fields|
|3|Start group|groups (deprecated)|
|4|End group|groups (deprecated)|
|5|32-bit|fixed32, sfixed32, float|
<!-- vale HouseStyle.Spelling = YES -->
<figcaption>Protobuf Wire Types</figcaption>

## Conclusion

The biggest problems when upgrading are mismatching required fields or a need to change field types. In the short term, adding other fields is a viable solution, but at a certain point, the marginal cost of that solution becomes more of a burden than auditing and upgrading your services.

Protocol Buffers are a relatively young technology, so changes now will have long-lasting implications. Compatibility issues do exist between versions, but they're possible to step around if you're careful. As always, make life simpler by planning out your data structures in advance. Once things eventually do change, the safest method for modifying fields is to add a new one and deprecate the old field.

To deprecate a field, you can change the name to something deprecated or remove it and reserve the identifier. If you really want to change a field type, and you're able to follow the correct version of [the rules](https://developers.google.com/protocol-buffers/docs/proto3#updating "Updating messages"), remember to never change the numerical identifier for that field. Plan well, and it'll be easy to maintain backward and forward compatibility for your Protocol Buffer deployment.

## Up Next

If you enjoyed this article, take a look at [Building a Monorepo in Golang](/blog/golang-monorepo/) or if you want to bring your CI to the next level then check out [Earthly](/).

{% include_html cta/bottom-cta.html %}
