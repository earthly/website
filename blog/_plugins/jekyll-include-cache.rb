# From https://github.com/benbalter/jekyll-include-cache/tree/main
# frozen_string_literal: true

require "jekyll"
require "digest/md5"

module JekyllIncludeCache
    class Tag < Jekyll::Tags::IncludeTag
      def self.digest_cache
        @digest_cache ||= {}
      end
  
      def render(context)
        path   = path(context)
        params = parse_params(context) if @params
        key = key(path, params)
        return unless path
  
        if JekyllIncludeCache.cache.key?(key)
          Jekyll.logger.debug "Include cache hit:", path
          JekyllIncludeCache.cache[key]
        else
          Jekyll.logger.debug "Include cache miss:", path
          JekyllIncludeCache.cache[key] = super
        end
      end
  
      private
  
      def path(context)
        site   = context.registers[:site]
        file   = render_variable(context) || @file
        locate_include_file(context, file, site.safe)
      end
  
      def key(path, params)
        path_hash   = path.hash
        params_hash = quick_hash(params)
        self.class.digest_cache[path_hash] ||= {}
        self.class.digest_cache[path_hash][params_hash] ||= digest(path_hash, params_hash)
      end

      def key_rich(path, params)
        params ||= {}
        # Check if a post object is included in the params
        if params[:post]
          post = params[:post]
          post_identifier = "#{post.slug}_#{post.last_modified_at.to_i}"
          # Create a unique identifier for the post to include in the cache key
          unique_post_part = stable_hash(post_identifier: post_identifier)
        else
          unique_post_part = ""
        end
        
        # Generate a hash for the remaining parameters, excluding the :post key manually
        remaining_params = params.reject { |k, _| k == :post }
        params_hash = stable_hash(remaining_params)
        
        # Combine path, post identifier (if any), and params hash into a final cache key
        "#{path}_#{unique_post_part}_#{params_hash}"
      end
      
      
      def stable_hash(params)
        Digest::MD5.hexdigest(params.to_s)
      end
      
      def quick_hash(params)
        return params.hash unless params
  
        md5 = Digest::MD5.new
  
        params.sort.each do |_, value|
          # Using the fact that Jekyll documents don't change during a build.
          # Instead of calculating the hash of an entire document (expensive!)
          # we just use its object id.
          if value.is_a? Jekyll::Drops::Drop
            md5.update value.object_id.to_s
          else
            md5.update value.hash.to_s
          end
        end
  
        md5.hexdigest
      end
  
      def digest(path_hash, params_hash)
        md5 = Digest::MD5.new
        md5.update path_hash.to_s
        md5.update params_hash.to_s
        md5.hexdigest
      end
    end
  end



module JekyllIncludeCache
  class << self
    def cache
      @cache ||= Jekyll::Cache.new(self.class.name)
    end

    def reset
       Jekyll.logger.info "JekyllIncludeCache:", "Caching is cleared." 
      JekyllIncludeCache.cache.clear
    end
  end
end

Jekyll::Hooks.register :site, :after_init do |site|
    if site.config["jekyll_include_cache"] && site.config["jekyll_include_cache"]["enabled"]
      Jekyll.logger.warn "JekyllIncludeCache:", "Caching is enabled."
      Liquid::Template.register_tag("include_cached", JekyllIncludeCache::Tag)
    # Here we can clear the cache, but it should not be needed
      # Jekyll::Hooks.register :site, :pre_render do |_site|
      #  JekyllIncludeCache.reset
      # end
    else
      Jekyll.logger.debug "JekyllIncludeCache:", "Caching is disabled."
      Liquid::Template.register_tag("include_cached", Jekyll::Tags::IncludeTag)
    end
end
