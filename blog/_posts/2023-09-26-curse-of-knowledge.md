---
title: "The Curse of Knowledge in Technical Writing"
categories:
  - Tutorials
toc: true
author: Mustapha Ahmad Ayodeji

internal-links:
 - curse of knowledge
 - knowledge in technical writing
 - curse in technical writing
 - technical writing
topcta: false
excerpt: |
    The article discusses the phenomenon of the Curse of Knowledge in technical writing, where authors assume that their audience possesses prior knowledge, leading to ineffective communication. It explores the causes of the curse, its impact on readers, and provides strategies for writers to overcome it and create clear and engaging technical content.
last_modified_at: 2023-10-06
---
<div class="align-right">
![]({{site.images}}{{page.slug}}/tFNsGfD.jpg)
<figcaption>The Professor</figcaption>
</div>

At the University of Ilorin, I once had a very knowledgeable professor. When he would come to class to lecture, his presence was always commanding and everyone would listen to him even before he would speak. He would lecture at a very abstract level, more of like a summary of the wealth of knowledge in his head. He would gesture expansively, flailing his usually oversized traditional attire as he tries to convey his complex idea, our confusion would be well written on our faces. Whenever he asked a question, the class always had blank faces because no one understood what he was saying. Then he would rant about how dull we were and why we couldn't understand these concepts that he thought were so basic. His voice would drip with the tone of condescension and frustration. For his subsequent classes, we would prepare really hard with the hope to keep up with his lecture, but no matter how hard we prepared, it was never enough to meet his expectations.

Later on, after working with the Django Framework for a while, I tried to explain the different components of the [Django framework](https://www.djangoproject.com/) like the [URL](https://docs.djangoproject.com/en/4.2/topics/http/urls/), [views](https://docs.djangoproject.com/en/4.2/topics/http/views/), and [models](https://docs.djangoproject.com/en/4.2/topics/db/models/) for a beginner that was just learning Django. I thought I was breaking down the concepts into manageable pieces, but the person's reaction made it clear we weren't on the same page. They would lean forward with furrowed eyebrows and frown faces with confusion written all over it.  

These experiences got me thinking and led me to search for a name for the scenario of a knowledgeable person struggling to explain to a novice. That's how I came across the phenomenon called the "Curse of Knowledge."

As a technical writer myself, whose job is to explain complex technical concepts to readers in a simple and easy-to-understand way, I couldn't help but imagine how this phenomenon affects the quality of the content I write as well as the quality of the content that other writers write.

In this article, I will discuss the phenomenon of the Curse of Knowledge and how it impacts technical writing, the causes of it, the effect on the readers of technical articles, and how writers can overcome it.

## What is the Curse of Knowledge

The [Curse of Knowledge](https://en.m.wikipedia.org/wiki/Curse_of_knowledge) refers to the cognitive bias in which an individual assumes that their audience possesses the prior knowledge necessary to understand a concept, leading to ineffective communication. This idea [was first introduced by economists [Colin Camerer]](https://en.m.wikipedia.org/wiki/Colin_Camerer), [George Loewenstein](https://en.m.wikipedia.org/wiki/George_Loewenstein), and [Martin Weber](https://en.m.wikipedia.org/w/index.php?title=Curse_of_knowledge&action=edit&section=1) in their research on the concept of the curse of knowledge and its economic implications. They found that better-informed parties are unable to ignore their better information.

This concept of curse of knowledge is observed in various fields, including academia, software engineering, and technical writing.

The Curse of knowledge in technical writing occurs when an author assumes that their audience has prior knowledge to understand their technical writing fully. This assumption can lead to technical writing that is unclear, ambiguous, and difficult to understand.

## Causes of Curse of Knowledge in Technical Writing

![Causes]({{site.images}}{{page.slug}}/cause.png)\

The curse of knowledge is generally [attributed to Fluency misattribution and Inhibition](https://www.sciencedirect.com/science/article/abs/pii/S0010027717301245?via%3Dihub).

Fluency misattribution is just a fancy name meaning that we (humans) think everyone can understand a subject matter easily because we can. It's really hard to imagine what its like to not know something you already know. Inhibition means it's hard for us to hold back our knowledge and adjust our perspective to that of our audience's making it hard to communicate effectively. Both of these causes can be particularly applicable to technical writing, where writers may be experts in their field and assume - without realizing it - that their readers have the same level of knowledge.

In addition to these two, some other causes of the curse of knowledge in technical writing include:

- Inadequate research of the intended audience: Researching the audience is a crucial step in technical writing as it helps writers to understand the needs and expectations of their readers. Researching the intended audience makes it easier for writers to consider the level of technical knowledge of their audience as this will allow them to know the level of technical jargon they can include in the article that the audience will comprehend. When writers do not research extensively about the intended audience of a technical article, their writings will likely be plagued with the curse of knowledge because they won't be fully aware of how much context is necessary.

- Lack of empathy: Technical writing requires empathy for the readers. Empathy helps writers understand and prioritize their audience's needs and take their perspectives into consideration, which in turn allows writers to create content that is more relevant and engaging. When writers are not empathetic with the readers, it will be hard to write with the readers in mind. Writers will tend to write based on their preferences rather than considering the needs of the readers. The articles will likely be full of technical jargon or fail to explain the intended concept in a way that the reader can understand. For example, a writer may use acronyms or technical terms that are unfamiliar to the reader, making the content less understandable.

Forgetting what it was like not to know: Writers often have good intentions, they just seem to forget what it was like not to know something. This means writers will not be able to give better explanations and communicate effectively.

Understanding these causes is essential for overcoming it. Next let's discuss impact.

## Impact of the Curse of Knowledge on Readers of Technical Writing

![Readers]({{site.images}}{{page.slug}}/readers.png)\

The curse of Knowledge can negatively impact the readers of technical writing in several ways. These include:

1. Poor understanding of technical articles

   All the points discussed in the causes of the curse of knowledge in technical writing will lead to readers' poor understanding of the technical article, and if it's an article that shows code examples or commands, the readers will merely copy and paste code snippets or commands, without fully grasping the underlying concepts or logic behind them.

   Proper understanding of new concepts takes some a while to understand, and articles that assume readers understand a concept they do not will not help them understand it.

2. Misinterpretation in technical writing:

   The curse of knowledge can lead to misinterpretation of the article. For example, when the writer does not provide the reason why instruction is necessary, the reader makes incorrect assumptions which can have negative consequences on the reader's ability to use or implement the information presented.

   The curse of knowledge can have significant negative impacts on the readers of technical writing. Poor understanding of technical articles and misinterpretation are some of the consequences that readers may face. However, there are ways to overcome this curse and improve the quality of technical writing. In the next section, I will discuss some strategies for writers to overcome the curse of knowledge and create technical content that is clear, concise, and engaging for readers.

## Overcoming Curse of Knowledge in Technical Article

![Overcoming]({{site.images}}{{page.slug}}/overcome.png)\

Overcoming the curse of knowledge totally is difficult, but writers can make an effort to reduce it.

While trying to overcome this mistake, writers need to focus on the audience while writing.

You can also eliminate the curse of knowledge in your content by performing various rounds of self-editing before publishing. While self-editing your article, you can leave the article for some days and come back to it with a fresh eye. When you come back to an article after a couple of days, some mistakes or assumptions that were not initially obvious become obvious and this will allow you to clarify some initial assumptions you made. You can also share the article with some intended audiences to get unbiased feedback. Perspectives from fresh eyes, especially the intended audience, make it easy to detect the curse of knowledge in technical content and eliminate it.

Furthermore, you can also overcome the curse of knowledge in technical writing by breaking down complex technical concepts into simpler language that can be easily understood by the intended audience. By using simple language that can be understood and relatable stories, you can help the readers grasp difficult concepts that might have otherwise been lost in jargon and technical terms. This approach not only helps overcome the curse of knowledge but also improves the overall clarity and effectiveness of technical writing.

Lastly, It is crucial to be fully conscious and present throughout the process of producing technical content. Elements of the curse of knowledge can creep into technical content when you are not fully engaged leading to assumptions about the readers' understanding, inadequate explanation, and context. Therefore, it is essential to approach technical writing with intentionality and focus ensuring that the content is clear and understandable.

## Conclusion

Now that you know all about the curse of knowledge, here's the best advice I can give you to avoid falling into this trap – to avoid being my old professor. First, put yourself in your readers' shoes - don't assume they know what you know. Break things down into simple pieces and explain concepts clearly. Second, get feedback from real readers - they'll let you know when you're losing them. And lastly, edit yourself ruthlessly - keep checking for jargon and assumptions.

If we make a real effort to see things from our readers' perspective, we can beat the curse of knowledge. Just remember to have empathy for your audience, and you'll be explaining things clearly in no time.

{% include_html cta/bottom-cta.html %}
