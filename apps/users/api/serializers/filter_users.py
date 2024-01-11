from django.forms import model_to_dict
from rest_framework import serializers

from user.models import User


class FilterUsersSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    hobbies = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = User.RANDOM_FILTERS_LIST

    def age(self, user):
        return user.age

    def get_main_image(self, user):
        media = user.main_image if user.main_image else user.created_profileimages.first()

        if media and media.media.name:
            return self.context['request'].build_absolute_uri(media.media.url)
        return None

    def get_images(self, user):
        images = user.created_profileimages.only('media')
        if user.id == "1ad0331e-30cb-43c7-8380-07bec75c800a":
            return [self.context['request'].build_absolute_uri(media.media.url) for media in images]
        import random
        images_list = [
            "https://img.freepik.com/free-photo/boy-expressing-his-happiness_23-2148155666.jpg?w=740&t=st=1701943269~exp=1701943869~hmac=b342c57152533c2889eb1d43139c794651d3d793c88198295f86a76af66361db",
            "https://source.unsplash.com/random/600x900",
            "https://img.freepik.com/free-photo/boy-expressing-his-happiness_23-2148155673.jpg?w=740&t=st=1701944309~exp=1701944909~hmac=c0d3a4142d53ba6f20edb921cc6cd6fa0b2a6baf3767909d2120a97c6df38d1c",
            "https://img.freepik.com/free-photo/boy-expressing-his-happiness_23-2148155664.jpg",
            "https://img.freepik.com/free-photo/joyful-young-pretty-woman-headphones-holds-looks-phone-isolated-orange-wall_141793-66401.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/group-friends-playing-video-games-home_23-2148560706.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/front-view-father-son-playing-console_23-2148350691.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/premium-photo/lifes-game-so-level-up-shot-young-man-cheering-while-playing-computer-games_590464-61569.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/high-angle-friends-playing-videogame_23-2149350034.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/teenagers-playing-videogames_23-2148105671.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/premium-photo/young-couple-enjoying-video-game-cellphone-against-blue-backdrop_23-2148056391.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/front-view-male-gamer-with-gamepad-playing-video-game-blue-wall_140725-152158.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/front-view-male-gamer-with-gamepad-headphones-playing-video-game-blue-wall_140725-152140.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/premium-photo/portrait-crazy-playful-gamer-boy-enjoying-playing-video-games-indoors-sitting-sofa-holding-console-gamepad-hands-resting-home-have-great-weekend_194143-842.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/close-up-portrait-little-blond-guy-wearing-casual-clothing-posing-with-headphones-around-neck-playing-online-video-games-via-mobile-phone-looks-concentrated-isolated-yellow_176532-9062.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/medium-shot-gamer-sitting-chair_23-2149829176.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/back-shot-happy-man-gamer-wining-first-person-shooter-video-game-playing-powerful-personal-computer-online-streaming-cyber-performing-during-gaming-tournament-using-technology-network-wireless_482257-12470.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/professional-esport-gamer-playing-game-tournament_53876-96330.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://img.freepik.com/free-photo/medium-shot-happy-man-playing-game_23-2149005173.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=ais",
            "https://t4.ftcdn.net/jpg/02/59/48/03/240_F_259480361_cYaWle6Onvl0ZceuKtwymtidaX3syhgR.jpg",
            "https://img.freepik.com/free-photo/happy-family-silhouette-sunset_1303-22466.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/happy-black-parents-with-kids-making-video-call-smart-phone-home_637285-11501.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/full-length-portrait-happy-young-african-family_171337-5044.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/full-length-portrait-happy-young-african-family_171337-5069.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/premium-photo/happy-family-home-spending-time-togethe_252847-36909.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/premium-photo/hes-got-us-smiling-from-ear-ear-cropped-portrait-affectionate-young-family-three-relaxing-sofa-their-living-room-home_590464-62510.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/parents-kids-spending-time-together_23-2149489597.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/full-length-portrait-smiling-family-with-child_171337-10331.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/full-length-portrait-smiling-family-with-child_171337-10331.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/premium-photo/family-is-forever-shot-family-bonding-sofa-home_590464-63227.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/photo-smiling-young-parents-with-little-child-lying-floor-isolated_186202-6413.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/cute-family-playing-summer-field_1157-36897.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/waist-up-portrait-handsome-serious-unshaven-male-keeps-hands-together-dressed-dark-blue-shirt-has-talk-with-interlocutor-stands-against-white-wall-self-confident-man-freelancer_273609-16320.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/portrait-handsome-smiling-stylish-young-man-model-dressed-red-checkered-shirt-fashion-man-posing_158538-4914.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/handsome-man-with-glasses_144627-18655.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/portrait-delighted-hipster-male-student-with-crisp-hair_176532-8157.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/indoor-picture-cheerful-handsome-young-man-having-folded-hands-looking-directly-smiling-sincerely-wearing-casual-clothes_176532-10257.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/bohemian-man-with-his-arms-crossed_1368-3542.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/shallow-focus-shot-young-attractive-male-posing-forest_181624-42367.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/young-bearded-man-with-striped-shirt_273609-5677.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
            "https://img.freepik.com/free-photo/isolated-image-positive-fashionable-young-man-with-stylish-hairdo-bristle-smiling-camera_343059-3558.jpg?size=626&ext=jpg&ga=GA1.1.388301907.1701943257&semt=sph",
        ]
        return random.choices(images_list, k=random.randint(2, 6))

    def get_state(self, user):
        if user.state:
            return model_to_dict(user.state, fields=('name_uz', 'name_en', 'name_ru'))

    def get_country(self, user):
        if user.country:
            return model_to_dict(user.country, fields=('name_uz', 'name_en', 'name_ru'))

    def get_hobbies(self, user):
        return user.hobbies.values('name_uz', 'name_ru', 'name_en')

    def get_reactions(self, user):
        return user.reactions.values('id', 'reaction', 'created_at')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'user_filters' in self.context:
            data['filters'] = self.context['user_filters']
        return data

    def get_likes(self, user):
        return user.likes
