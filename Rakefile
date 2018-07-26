#!/usr/bin/rake -T

require 'simp/rake'
require 'simp/rake/pupmod/helpers'
require 'yaml'

Simp::Rake::Pkg.new( File.dirname( __FILE__ ) )

task :yaml_validate do
  Dir.glob('environments/simp/**/*.{yaml,yml}').each do |f|
    y = YAML.load_file(f)
    if (y.nil?) or (y == false)
      abort("File #{f} is invalid")
    end
  end
end
