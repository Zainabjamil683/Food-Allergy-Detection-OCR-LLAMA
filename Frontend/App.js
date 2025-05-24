import React, { useState, useEffect } from "react";
import { View, ActivityIndicator, TouchableOpacity, Image } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { auth } from "./src/firebaseConfig";
import { onAuthStateChanged } from "firebase/auth";

// Import Screens
import SplashScreen from "./src/screens/SplashScreen"; // ✅ Keep this
import HomeScreen from "./src/screens/HomeScreen";
import LoginScreen from "./src/screens/LoginScreen";
import SignUpScreen from "./src/screens/SignUpScreen";
import ProfileInfoScreen from "./src/screens/ProfileInfoScreen";
import AllergyDetailsScreen from "./src/screens/AllergyDetailsScreen";
import SuccessScreen from "./src/screens/SuccessScreen";
import ErrorScreen from "./src/screens/ErrorScreen";
import WelcomeScreen from "./src/screens/WelcomeScreen";
import DashboardScreen from "./src/screens/DashboardScreen";
import AccountScreen from "./src/screens/AccountScreen";
import QuizScreen from "./src/screens/QuizScreen";

const Stack = createStackNavigator();

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
        <ActivityIndicator size="large" color="#008D70" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Splash">
        <Stack.Screen
          name="Splash"
          component={SplashScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Welcome" component={WelcomeScreen} />
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
        <Stack.Screen name="ProfileInfo" component={ProfileInfoScreen} />
        <Stack.Screen
          name="AllergyDetails"
          component={AllergyDetailsScreen}
          options={({ navigation }) => ({
            title: "Allergy Details",
            headerRight: () => (
              <TouchableOpacity onPress={() => navigation.navigate("Account")}>
                <Image
                  source={require("./assets/info_icon.png")}
                  style={{ width: 24, height: 24, marginRight: 15 }}
                />
              </TouchableOpacity>
            ),
          })}
        />
        <Stack.Screen name="Quiz" component={QuizScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="SignUp" component={SignUpScreen} />
        <Stack.Screen name="Success" component={SuccessScreen} />
        <Stack.Screen name="Error" component={ErrorScreen} />
        <Stack.Screen name="Account" component={AccountScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
