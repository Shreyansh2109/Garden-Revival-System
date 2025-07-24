const mongoose = require("mongoose");

const GarbageSchema = new mongoose.Schema({
    garbage_type: { type: String, required: true },  // Type of garbage
    weight_kg: { type: Number, required: true },     // Weight in kg
    timestamp: { type: Date, default: Date.now }     // Timestamp of collection
});

module.exports = mongoose.model("GarbageCollection", GarbageSchema);
