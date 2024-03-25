module Jekyll
    class PostIndexGenerator < Generator
      priority :highest
  
      def generate(site)
        start_time = Time.now  # Capture start time
  
        # Initialize empty hashes for each index
        slug_index = {}
        author_index = {}
        editor_index = {}
        topic_index = {}
        funnel_index = {}
        related_index = {}
  
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
          if funnel > 0
            (funnel_index[funnel] ||= []) << post
          end
        end

        # Build the related_index
        if site.data['related_articles']
            site.data['related_articles'].each do |slug, related_slugs|
              related_posts = related_slugs.map { |related_slug| slug_index[related_slug] }.compact
              related_index[slug] = related_posts
            end
          end

  
        # Store the indexes in site.data for access in templates
        site.data['indexes'] = {
          'slug' => slug_index,
          'author' => author_index,
          'editor' => editor_index,
          'topic' => topic_index,
          'funnel' => funnel_index,
          'related' => related_index
        }
  
        end_time = Time.now  # Capture end time
        duration = end_time - start_time  # Calculate duration
  
        Jekyll.logger.debug "PostIndexGenerator:", "Indexes built in #{duration} seconds"
      end
    end
  end
  