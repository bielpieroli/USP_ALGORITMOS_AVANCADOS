#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <iomanip>
#include <limits>

using namespace std;

const double EARTH_RADIUS = 6371.0;
const double PI = 3.14159265358979323846;
const double INF = numeric_limits<double>::infinity();

double transformDegreesIntoRadian(double coord)
{
  return coord * PI / 180.0;
}

double haversine(double correctLat, double correctLon, double guessedLat, double guessedLon)
{
  double innerRoot = pow(sin((guessedLat - correctLat) / 2.0), 2) +
                     cos(guessedLat) * cos(correctLat) *
                         pow(sin((guessedLon - correctLon) / 2.0), 2);
  double dist = 2.0 * EARTH_RADIUS * asin(sqrt(innerRoot));
  return dist;
}

double calculateDistance(double correctLat, double correctLon, double guessedLatDegrees, double guessedLonDegrees)
{
  double guessedLatRad = transformDegreesIntoRadian(guessedLatDegrees);
  double guessedLonRad = transformDegreesIntoRadian(guessedLonDegrees);
  return haversine(correctLat, correctLon, guessedLatRad, guessedLonRad);
}

int main()
{
  int numberOfPlayers;
  cin >> numberOfPlayers;

  double correctLat;
  double correctLon;

  cin >> correctLat;
  cin >> correctLon;

  correctLat = transformDegreesIntoRadian(correctLat);
  correctLon = transformDegreesIntoRadian(correctLon);

  priority_queue<pair<double, string>,
                 vector<pair<double, string>>,
                 greater<pair<double, string>>>
      guesses;

  double bestGuessedDist = INF;
  string name;
  double latDegrees;
  double lonDegrees;

  for (int i = 0; i < numberOfPlayers; i++)
  {

    cin >> name;
    cin >> latDegrees;
    cin >> lonDegrees;

    // cout << name << endl;
    // cout << latDegrees << endl;
    // cout << lonDegrees << endl;

    double dist = calculateDistance(correctLat, correctLon, latDegrees, lonDegrees);

    if (bestGuessedDist > dist)
    {
      bestGuessedDist = dist;
    }

    cout << "> [AVISO] MELHOR PALPITE: " << fixed << setprecision(3)
         << bestGuessedDist << "km" << endl;

    guesses.push({dist, name});
  }

  cout << endl;
  cout << "RANKING" << endl;
  cout << "-------" << endl;

  for (int i = 1; i <= numberOfPlayers; i++)
  {
    auto guess = guesses.top();
    guesses.pop();

    double dist = guess.first;
    string name = guess.second;

    printf("%2d. %-20s : %6.3f km", i, name.c_str(), dist);

    if (dist < 0.050)
    {
      printf(" [FANTASTICO]");
    }

    printf("\n");
  }
  return 0;
}