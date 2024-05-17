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
        related_sidebar = {}
        popular_sidebar = {}
        related_footer = {}
        shorten_name = {}
  
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

          short_title = site.data['short_titles'][slug]
          if short_title
            shorten_name[slug] = short_title
          end
        
          # Index by funnel
          funnel = post.data['funnel']
          if funnel > 0
            (funnel_index[funnel] ||= []) << post
          end
        end

        # Build the related_index
        funnel_3_sample = funnel_index[3] ? funnel_index[3].shuffle : []
        fall_back_popular = []

        site.posts.docs.each do |post|
          slug = post.data['slug'] || post.slug
          related_slugs = site.data['related_articles'][slug]
          
          if related_slugs
            # If there are explicitly related articles listed
            related_posts = related_slugs.map { |related_slug| slug_index[related_slug] }.compact
          else
            # Initialize as empty if there are no explicitly related articles
            related_posts = []
          end
          
          related_sidebar[slug] = related_posts.dup

          if related_posts.length < 2
            # Calculate how many posts are needed to pad the related list to 2 items
            padding_needed = 2 - related_posts.length
            padding_posts = funnel_3_sample.sample(padding_needed) if !funnel_3_sample.empty?
            related_posts.concat(padding_posts) if padding_posts
          end
        
          # Assign the padded or filled list of related posts to the related_index for the slug
          related_footer[slug] = related_posts.uniq.take(2)

          popular_slugs = site.data['related_popular_articles'][slug]

          if popular_slugs
            # If there are explicitly related articles listed
            popular_posts = popular_slugs.map { |related_slug| slug_index[related_slug] }.compact
          else
            # Initialize as empty if there are no explicitly related articles
            Jekyll.logger.debug "No popular found for:", slug
            popular_posts = fall_back_popular
          end
          
          popular_sidebar[slug] = popular_posts.dup
          fall_back_popular = popular_posts
        end
  
        # Store the indexes in site.data for access in templates
        site.data['indexes'] = {
          'slug' => slug_index,
          'author' => author_index,
          'editor' => editor_index,
          'topic' => topic_index,
          'funnel' => funnel_index,
          'related_sidebar' => related_sidebar,
          'popular_sidebar' => popular_sidebar,
          'related_footer' => related_footer,
          'shorten_name' => shorten_name,
        }
  
        end_time = Time.now  # Capture end time
        duration = end_time - start_time  # Calculate duration
  
        Jekyll.logger.debug "PostIndexGenerator:", "Indexes built in #{duration} seconds"
      end
    end
  end
  