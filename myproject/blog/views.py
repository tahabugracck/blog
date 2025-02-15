from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import Post

# Blog Yazıları Listesi
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Tüm blog yazılarını en yeniye göre sıralıyoruz
    return render(request, 'blog/post_list.html', {'posts': posts})

# Blog Yazısının Detayı
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # ID'ye göre blog yazısını al
    return render(request, 'blog/post_detail.html', {'post': post})

# PostForm - Blog Yazısı Formu
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Kullanıcı sadece başlık ve içerik girecek

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise forms.ValidationError('Başlık 100 karakteri geçemez.')
        return title

# Yeni Blog Yazısı Ekleme
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')  # Yazı kaydedildikten sonra ana sayfaya yönlendir
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})

# Blog Yazısını Güncelleme
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # ID'ye göre blog yazısını al
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # Mevcut yazıyı düzenliyoruz
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)  # Güncellendikten sonra detay sayfasına yönlendir
    else:
        form = PostForm(instance=post)  # Formu doldur, mevcut veriyi göster

    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

# Blog Yazısını Silme
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # ID'ye göre blog yazısını al
    if request.method == 'POST':  # Kullanıcı silmeyi onayladı mı?
        post.delete()
        return redirect('post_list')  # Silindikten sonra ana sayfaya yönlendir

    return render(request, 'blog/post_confirm_delete.html', {'post': post})
