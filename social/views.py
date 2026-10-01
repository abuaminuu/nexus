from datetime import timezone
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import json
from django.http import JsonResponse

from .models import User, Post, Follow, Profile


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    page_numner = request.GET.get("page")
    
    try:
        page_object = paginator.get_page(page_numner)
    except PageNotAnInteger:
        page_object = paginator.get_page(1)
    except EmptyPage:
        page_object = paginator.get_page(paginator.num_pages)


    return render(request, "social/index.html", {
        "page_object": page_object,
    })


# get the content of the post and save it to the database
def post(request):
    # only auth user can post.
    if request.method == "POST" and request.user.is_authenticated:
        # get content of the post
        content = request.POST["content"]
        
        if content.strip() == "":
            return render(request, "social/post.html", {
                "error": "Post content cannot be empty.",
            })
        
        try:
            # create the data
            Post.objects.create(user=request.user, content=content)
            return redirect("index")
        
        except Exception as e:
            return render(request, "social/post.html", {
                "error":f"error while posting: {content} {e}",
            })

    else:
        return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(f"User '{username}' does not exist.")


    posts = Post.objects.filter(user=user).order_by("-timestamp")
    following = Follow.objects.filter(follower=user).count()
    followers = Follow.objects.filter(following=user).count()
    is_following = None
    
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    
    try:
        page_object = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_object = paginator.get_page(1)
    except EmptyPage:
        page_object = paginator.get_page(paginator.num_pages)


    return render(request, "social/profile.html", {
        "profile": user,
        "page_object": page_object,
        "following":following,
        "followers":followers,
        "is_following": is_following,
        "bio": user.profile.bio if hasattr(user, 'profile') else 'no bio yet!',
        "profile_picture_url": user.profile.profile_picture.url if hasattr(user, 'profile') and user.profile.profile_picture else None,
    })
    

def following(request):

    # get list of users this user follows
    following_ids = Follow.objects.filter(follower=request.user.id).values_list("following", flat=True)
    
    # all posts from the users this user currently follows and their posts
    followings = User.objects.filter(id__in=following_ids)
    posts = Post.objects.filter(user__in=following_ids).order_by("-timestamp")
    # 5 random users NOT followed and NOT the current user
    suggested_users = User.objects.exclude(id__in=following_ids).exclude(id=request.user.id).order_by('?')[:5]
    
    return render(request, "social/following.html", {
        "posts": posts,
        "followings": followings,
        "suggested_users": suggested_users,
    })


def follow(request, username):
    # only post allowed
    # create a follow relationship between the auth user and this username
    if request.user.is_authenticated and request.user.username != username:
        try:
            following_user = User.objects.get(username=username)
            Follow.objects.create(follower=request.user, following=following_user)
            return redirect("profile", username=username)
        
        except Exception as e:
            return HttpResponse(f"error while {request.user} Yfollowing {username}: {e}")
    else:
        return HttpResponseRedirect(reverse("login"))
    

def unfollow(request, username):
    # only POST allowed
    # delete the follow relationship between the auth user and this username
    if request.user.is_authenticated and request.user.username != username:
        try:
            following_user = User.objects.get(username=username)
            Follow.objects.filter(follower=request.user, following=following_user).delete()
            return redirect("profile", username=username)
        
        except Exception as e:
            return HttpResponse(f"error while {request.user} uXnfollowing {username}: {e}")
    else:
        return HttpResponseRedirect(reverse("index"))


# endpoint to edit a post
def edit_post(request, post_id):

    if request.method == "POST" and request.user.is_authenticated:
        try:
            post = Post.objects.get(id=post_id)
            # check if the user is the owner of the post
            if post.user != request.user:
                return JsonResponse({"error": "You are not allowed to edit this post."}, status=403)
            
            # get the new content from the request
            data = json.loads(request.body)
            new_content = data.get("content", "").strip()
            post.content = new_content
            post.save()

            return JsonResponse({
                "message": "Post updated successfully.",
                "success": True,
                }, status=200)
        
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post does not exist."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Error while editing post: {e}"}, status=400)
    
    else:
        return JsonResponse({"error": "Invalid request method or user not authenticated."}, status=400) 
    
def like_post(request, post_id):
    #  post.user -> the user who created the post
    # request.user -> the user who is liking the post
    
    if request.method == "POST" and request.user.is_authenticated:
        try:
            # get post object
            post = Post.objects.get(id=post_id)

            # user cant not like their own post
            if post.user == request.user:
                return JsonResponse({
                    "message":"you cant like your own post!",
                    "success": False
                }, status=400)

            # does this user liked the post before?
            like_exists = post.like_by.filter(id=request.user.id).exists()

            if like_exists == True:
                # remove the user from the like_by field
                post.like_by.remove(request.user)

                return JsonResponse({
                    "message":"removed ! you liked this post already",
                    "success": True,
                    "like_status": post.like_status(request.user),
                    "like_count": post.like_count(),
                    }, status=201)
            
            if like_exists == False:
                # update with user object who liked the post
                post.like_by.add(request.user)
            
                return JsonResponse({
                    "message": "post liked updated/added!",
                    "success": True,
                    "like_status": post.like_status(request.user),
                    "like_count": post.like_count(),
                }, status=201)
            
        except Post.DoesNotExist:

            return JsonResponse({
                "message": "post: " + post_id + " does not exist !",
                "success": False
                }, status=404)
    else:
        return JsonResponse({"error": "you are not authenticated !"}, status=405)

# update posts endpoint
def edit_profile(request):

    if request.method == "POST" and request.user.is_authenticated:
        try:
            bio = request.POST.get("bio", "")
            if bio:
                bio.strip()
            
            # buid default dynamically with bio
            update_fields = {"bio": bio, }

            if "profile_picture" in request.FILES:
                # add to dict
                update_fields['profile_picture'] =  request.FILES["profile_picture"]

            # create profile if it does not exist
            profile, created = Profile.objects.update_or_create(
                user=request.user,
                defaults = update_fields
            )

            return JsonResponse({
                "message": "Profile updated successfully.",
                "success": True,
                "bio": profile.bio,
                "profile_picture_url": profile.profile_picture.url if profile.profile_picture else None,
            }, status=200)
        
        except Exception as e:
            return JsonResponse({
                "message": f"Error while editing profile: {e}",
                "success": False,
            }, status=400)
    
    else:
        # only allow POST requests from the authenticated user who owns the profile
        return JsonResponse({
            "message": "Invalid request method or user not authenticated.",
            "success": False,
        }, status=400)

