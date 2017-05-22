from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from flask import request, jsonify
from app.models import User, Role, CurrentNews, WorkTrends, Activity, PartyMember, LearnContent, Comment
from flask import current_app
from flask import abort, flash
from .forms import CommentForm
from flask_login import current_user


# todo 首页都展示哪些数据？？

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    首页
    :return:
    """
    # 时事要闻 8条
    # news = CurrentNews.query.order_by(CurrentNews.publish_time).limit(8).all()
    #
    # work_trends = WorkTrends.query.order_by(WorkTrends.publish_time).limit(8).all()
    #
    # activity = Activity.query.order_by(Activity.publish_time).limit(8).all()

    # return render_template('index.html', current_news=news, work_trends=work_trends, activity=activity)
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    """
    查看user详情
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/news', methods=['GET'])
def current_news():
    """
    实事要闻
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = CurrentNews.query.order_by(CurrentNews.publish_time).paginate(
            page, per_page=current_app.config['PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('main/news.html', posts=posts,
                           pagination=pagination)


@main.route('/news/<int:pk>', methods=['GET', 'POST'])
def current_news_detail(pk):
    """
    实事要闻detail
    :return:
    """
    post = CurrentNews.query.get(pk)
    object_type = CurrentNews.__tablename__
    object_id = pk
    form = CommentForm()
    if form.validate_on_submit():

        comment = Comment(content=form.content.data, author=current_user._get_current_object(),
                          object_type=object_type, object_id=object_id)
        db.session.add(comment)
        flash('You comment has been published')
        # 跳转到最新评论页
        return redirect(url_for('main.current_news_detail', pk=pk, page=-1))
    #
    page = request.args.get('page', 1, type=int)
    comment_owned = Comment.query.filter_by(object_type=object_type, object_id=object_id)

    if page == -1:
        page = comment_owned.count() - 1 / \
            current_app.config['PER_PAGE'] + 1

    pagination = comment_owned.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config['PER_PAGE'],
                                                                          error_out=False)
    comments = pagination.items
    return render_template('main/news_detail.html', posts=post, form=form, comments=comments, pagination=pagination)


@main.route('/trends', methods=['GET'])
def work_trends():
    """
    工作动态
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = WorkTrends.query.order_by(WorkTrends.publish_time).paginate(
            page, per_page=current_app.config['PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('main/trends.html', posts=posts,
                           pagination=pagination)


@main.route('/trends/<int:pk>', methods=['GET'])
def work_trends_detail(pk):
    """
    工作动态detail
    :param pk:
    :return:
    """
    post = WorkTrends.query.get(pk)
    object_type = WorkTrends.__tablename__
    object_id = pk
    form = CommentForm()
    if form.validate_on_submit():

        comment = Comment(content=form.content.data, author=current_user._get_current_object(),
                          object_type=object_type, object_id=object_id)
        db.session.add(comment)
        flash('You comment has been published')
        # 跳转到最新评论页
        return redirect(url_for('main.current_news_detail', pk=pk, page=-1))
    #
    page = request.args.get('page', 1, type=int)
    comment_owned = Comment.query.filter_by(object_type=object_type, object_id=object_id)

    if page == -1:
        page = comment_owned.count() - 1 / \
            current_app.config['PER_PAGE'] + 1

    pagination = comment_owned.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config['PER_PAGE'],
                                                                          error_out=False)
    comments = pagination.items
    return render_template('main/trends_detail.html', posts=post, form=form, comments=comments, pagination=pagination)


@main.route('/activities', methods=['GET'])
def activities():
    """
    活动集锦
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = Activity.query.order_by(Activity.publish_time).paginate(
            page, per_page=current_app.config['PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('main/activities.html', posts=posts,
                           pagination=pagination)


@main.route('/activities/<int:pk>', methods=['GET'])
def activities_detail(pk):
    """
    活动集锦detail
    :param pk:
    :return:
    """
    post = Activity.query.get(pk)
    object_type = Activity.__tablename__
    object_id = pk
    form = CommentForm()
    if form.validate_on_submit():

        comment = Comment(content=form.content.data, author=current_user._get_current_object(),
                          object_type=object_type, object_id=object_id)
        db.session.add(comment)
        flash('You comment has been published')
        # 跳转到最新评论页
        return redirect(url_for('main.current_news_detail', pk=pk, page=-1))
    #
    page = request.args.get('page', 1, type=int)
    comment_owned = Comment.query.filter_by(object_type=object_type, object_id=object_id)

    if page == -1:
        page = comment_owned.count() - 1 / \
            current_app.config['PER_PAGE'] + 1

    pagination = comment_owned.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config['PER_PAGE'],
                                                                          error_out=False)
    comments = pagination.items
    return render_template('main/activities_detail.html', posts=post, form=form, comments=comments,
                           pagination=pagination)


@main.route('/party_members', methods=['GET'])
def party_members():
    """
    党员风采
    :return:
    """
    page = request.args.get('page', 1, type=int)
    pagination = PartyMember.query.order_by(PartyMember.publish_time).paginate(
            page, per_page=current_app.config['PER_PAGE'],
            error_out=False)
    posts = pagination.items
    return render_template('main/party_members.html', posts=posts,
                           pagination=pagination)


@main.route('/party_members/<int:pk>', methods=['GET'])
def party_members_detail(pk):
    """
    党员风采detail
    :param pk:
    :return:
    """
    post = PartyMember.query.get(pk)
    object_type = PartyMember.__tablename__
    object_id = pk
    form = CommentForm()
    if form.validate_on_submit():

        comment = Comment(content=form.content.data, author=current_user._get_current_object(),
                          object_type=object_type, object_id=object_id)
        db.session.add(comment)
        flash('You comment has been published')
        # 跳转到最新评论页
        return redirect(url_for('main.current_news_detail', pk=pk, page=-1))
    #
    page = request.args.get('page', 1, type=int)
    comment_owned = Comment.query.filter_by(object_type=object_type, object_id=object_id)

    if page == -1:
        page = comment_owned.count() - 1 / \
            current_app.config['PER_PAGE'] + 1

    pagination = comment_owned.order_by(Comment.timestamp.asc()).paginate(page, per_page=current_app.config['PER_PAGE'],
                                                                          error_out=False)
    comments = pagination.items
    return render_template('main/party_members_detail.html', posts=post, form=form, comments=comments,
                           pagination=pagination)


@main.route('/learn_content', methods=['GET'])
def learn_content():
    """
    学习内容
    :param pk:
    :return:
    """
    return render_template('/main/learn_content.html')


# 分类 0: 重要文件 1:理论学习 2:报刊社论
@main.route('/important_file_video', methods=['GET'])
def important_file_video():
    """
    重要文件 video形式
    :return: json
    """
    data = LearnContent.query.filter_by(classtype=0, learntype=0).order_by(LearnContent.publish_time).limit(4)
    result = {'data': [i._pack_data() for i in data], 'result': 'OK'}
    return jsonify(result)


@main.route('/important_file_text', methods=['GET'])
def important_file_text():
    """
    重要文件 文本形式
    :return: json
    """
    data = LearnContent.query.filter_by(classtype=0, learntype=1).order_by(LearnContent.publish_time).limit(4)
    result = {'data': [i._pack_data() for i in data], 'result': 'OK'}
    return jsonify(result)


@main.route('/theory_video', methods=['GET'])
def theory_video():
    """
    理论学习 video形式
    :return: json
    """
    data = LearnContent.query.filter_by(classtype=1, learntype=0).order_by(LearnContent.publish_time).limit(4)
    result = {'data': [i._pack_data() for i in data], 'result': 'OK'}
    return jsonify(result)


@main.route('/theory_text', methods=['GET'])
def theory_text():
    """
    理论学习 文本形式
    :return: json
    """
    data = LearnContent.query.filter_by(classtype=1, learntype=1).order_by(LearnContent.publish_time).limit(4)
    result = {'data': [i._pack_data() for i in data], 'result': 'OK'}
    return jsonify(result)


@main.route('/paper_video', methods=['GET'])
def paper_video():
    """
    报刊社论 video形式
    :return: json
    """
    data = LearnContent.query.filter_by(classtype=2, learntype=0).order_by(LearnContent.publish_time).limit(4)
    result = {'data': [i._pack_data() for i in data], 'result': 'OK'}
    return jsonify(result)


@main.route('/paper_text', methods=['GET'])
def paper_text():
    """
    报刊社论 文本形式
    :return: json
    """
    data = LearnContent.query.filter_by(classtype=2, learntype=1).order_by(LearnContent.publish_time).limit(4)
    result = {'data': [i._pack_data() for i in data], 'result': 'OK'}
    return jsonify(result)






