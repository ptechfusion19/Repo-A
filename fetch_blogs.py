"""
Fetch blog slugs and IDs from the ProgrammX API
"""

import requests
import json


def fetch_blogs(published: bool = True) -> list[dict]:
    """
    Fetch blogs from the ProgrammX API.
    
    Args:
        published: If True, fetch only published blogs
        
    Returns:
        List of blog dictionaries with id and slug
    """
    url = "https://programmx.com/api/blogs"
    params = {"published": str(published).lower()}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # The API returns a structure with 'data' array
        blogs = data.get("data", [])
        
        # Extract only id and slug from each blog
        result = []
        for blog in blogs:
            result.append({
                "id": blog.get("_id"),
                "slug": blog.get("slug")
            })
        
        return result
        
    except requests.RequestException as e:
        print(f"Error fetching blogs: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return []


def main():
    print("Fetching published blogs from ProgrammX API...")
    print("-" * 50)
    
    blogs = fetch_blogs(published=True)
    
    if not blogs:
        print("No blogs found or error occurred.")
        return
    
    print(f"Found {len(blogs)} blogs:\n")
    
    for i, blog in enumerate(blogs, 1):
        print(f"{i}. ID: {blog['id']}")
        print(f"   Slug: {blog['slug']}")
        print()
    
    # Also save to a JSON file for reference
    output_file = "blogs_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(blogs, f, indent=2)
    
    print(f"Data saved to {output_file}")


if __name__ == "__main__":
    main()

