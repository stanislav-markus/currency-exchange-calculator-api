from collections import defaultdict

from django.contrib.auth.models import User, Group
from django_filters.rest_framework import DjangoFilterBackend
from calculator.api.models import CurrencyRate, CurrencyPair
from rest_framework import viewsets
from rest_framework import permissions
from calculator.api.serializers import UserSerializer, GroupSerializer, CurrencyPairSerializer, CurrencyRateSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrencyPairViewSet(viewsets.ModelViewSet):
    queryset = CurrencyPair.objects.all()
    serializer_class = CurrencyPairSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrencyRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRate.objects.all()
    serializer_class = CurrencyRateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'pair__code']

    def get_queryset(self):
        queryset = self.queryset
        connections = []
        requested_date = self.request.query_params.get('date')
        requested_code = self.request.query_params.get('pair__code')
        if not CurrencyPair.objects.filter(code=requested_code).exists():
            if not requested_date:
                raise Exception("Date is required")
            for pair in CurrencyPair.objects.all():
                connections.append(pair.code.split('/'))
            graph = self.__create_graph(connections)
            orig, dest = requested_code.split('/')
            shortest_way = self.__get_shortest_way(graph, orig, dest)
            if shortest_way:
                path = []
                for i in range(len(shortest_way)):
                    if i < len(shortest_way)-1:
                        path.append('/'.join([shortest_way[i], shortest_way[i+1]]))
                result = 1
                for code in path:
                    if CurrencyPair.objects.filter(code=code).exists():
                        result *= CurrencyRate.objects.get(date=requested_date, pair__code=code).rate
                    else:
                        rev_code = '/'.join(code.split('/')[::-1])
                        result *= 1 / CurrencyRate.objects.get(date=requested_date, pair__code=rev_code,).rate
                queryset = queryset.filter(date=requested_date)
                pair = CurrencyPair.objects.first()
                pair.code = requested_code
                queryset.update(rate=result, pair=pair)
        return queryset

    def __create_graph(self, connections):
        graph = defaultdict(list)
        for orig, dest in connections:
            graph[orig].append(dest)
            graph[dest].append(orig)
        return graph

    def __get_shortest_way(self, graph, orig, dest):
        way = []
        queue = [[orig]]
        if orig == dest:
            return None
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in way:
                connections = graph[node]
                for connection in connections:
                    new_path = list(path)
                    new_path.append(connection)
                    queue.append(new_path)
                    if connection == dest:
                        return new_path
                way.append(node)
        return None
