


@task
def describe_conversation(conversation: List[str]) -> str:
    """
    create a one liner description of the conversation
    :param conversation: the provided conversation
    :return: A one liner description of the conversation
    """
    return magic(conversation)



@search
def get_relevant_blog_posts(query: str, data: SemanticData) -> List[str]:
    """
    Find the relevant blog posts
    :param query: A use provided query to search with
    :param data: A semantic data object that contains the blog posts
    :return: The relevant blog posts
    """
    return magic(query, data)


@task
def rank_blog_posts(query: str, blog_posts: List[str]) -> List[str]:
    """
    Rank the blog posts based on the given query
    :param query: A use provided query to rank the blog posts with
    :param blog_posts: A list of blog posts to rank
    :return: A list of the ranked blog posts
    """
    return magic(query, blog_posts)


def conversation_to_suggested_blogposts(conversation, data) -> str:
    one_liner = describe_conversation(conversation=conversation)
    relevant_blog_posts = get_relevant_blog_posts(query=one_liner, data=data)
    ranked_blog_posts = rank_blog_posts(query=one_liner, blog_posts=relevant_blog_posts)
    return ranked_blog_posts
