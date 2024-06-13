module Jekyll
  class CategoryPageGenerator < Generator
    safe true

    def generate(site)
      if site.layouts.key? 'category'
        site.data['categories'].each do |category|
            category['items'].each do |item|
              site.pages << CategoryPage.new(site, site.source, item['slug'], item['name'], item['title'])
            end
        end
      end
    end
  end

  class CategoryPage < Page
    def initialize(site, base, slug, name, title)
      @site = site
      @base = base
      @dir  = "categories/#{slug}"
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'category.html')
      self.data['title'] = title
      self.data['slug'] = slug
      self.data['permalink'] = "/categories/#{slug}/"
      self.data['category_name'] = name
    end
  end
end
