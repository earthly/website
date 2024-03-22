module Jekyll
    class PostIndexGenerator < Generator
      priority :highest
  
      def generate(site)
        # Initialize empty hashes for each index
        slug_index = {}
        author_index = {}
        editor_index = {}
        topic_index = {}
        funnel_index = {}
  
        # Iterate over each post to populate the indexes
        site.posts.docs.each do |post|
          # Index by slug
          slug = post.data['slug'] || post.slug
          slug_index[slug] = post
  
          # Index by author
          author = post.data['author']
          (author_index[author] ||= []) << post
  
          # Index by editor
          editor = post.data['editor']
          (editor_index[editor] ||= []) << post
  
          # Index by topic
          topic = post.data['topic']
          (topic_index[topic] ||= []) << post
        
          # Index by funnel
          funnel = post.data['funnel']
          (topic_index[funnel] ||= []) << post
        end
  
        # Store the indexes in site.data for access in templates
        site.data['indexes'] = {
          'slug' => slug_index,
          'author' => author_index,
          'editor' => editor_index,
          'topic' => topic_index,
          'funnel' => funnel_index,
        }
      end
    end
  end
  