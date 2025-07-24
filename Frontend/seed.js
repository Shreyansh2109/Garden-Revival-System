const mongoose = require("mongoose");
const GarbageCollection = require("./models/garbageModel"); // Import schema

// ✅ Replace with your MongoDB Atlas connection string
const MONGO_URI = "mongodb+srv://sshreyansh2103:sshreyansh2103@cluster0.p58xg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

// ✅ Connect to MongoDB Atlas
mongoose.connect(MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
.then(() => console.log("✅ Connected to MongoDB Atlas"))
.catch(err => console.error("❌ MongoDB Connection Error:", err));

// ✅ Fake Data Generation
const fakeGarbageData = [
    {
        "garbage_type": "Garbage",
        "weight_kg": 1.26,
        "timestamp": "2025-02-08T06:14:04.291+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 2.45,
        "timestamp": "2025-02-08T07:30:15.123+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 3.78,
        "timestamp": "2025-02-08T08:45:27.567+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 0.95,
        "timestamp": "2025-02-08T09:12:10.432+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 1.89,
        "timestamp": "2025-02-08T10:25:33.876+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 2.15,
        "timestamp": "2025-02-08T11:50:42.345+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 3.05,
        "timestamp": "2025-02-08T12:40:55.123+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 1.63,
        "timestamp": "2025-02-08T13:20:18.654+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 2.77,
        "timestamp": "2025-02-08T14:35:29.987+00:00"
    },
    {
        "garbage_type": "Garbage",
        "weight_kg": 0.82,
        "timestamp": "2025-02-08T15:10:40.789+00:00"
    }
];

// ✅ Insert Fake Data
const insertFakeData = async () => {
    try {
        await GarbageCollection.insertMany(fakeGarbageData);
        console.log("✅ Fake garbage data inserted successfully!");
        mongoose.connection.close(); // Close connection after insertion
    } catch (error) {
        console.error("❌ Error inserting data:", error);
    }
};

// ✅ Run the function
insertFakeData();
