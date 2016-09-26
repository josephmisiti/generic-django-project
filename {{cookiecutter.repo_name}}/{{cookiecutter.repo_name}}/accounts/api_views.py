class LoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        if request.user.is_authenticated():
            data = UserSerializer(request.user).data
            return Response(data)

        form = LoginForm(request.DATA)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth.login(request, user)
            data = serializers.UserSerializer(user).data
            return Response(data)
        else:
            return Response({ 'errors': form.errors }, status=400)


class LogoutView(APIView):
    """ 
    > Session based API logout
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        auth.logout(request)
        return Response(status=200)
        
        