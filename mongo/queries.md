## Queries example

// Count documents
/db.summary.countDocuments()

// Inspect one document
/db.summary.findOne()

// Sample first 5 documents
/db.summary.find().limit(5)

// Distinct categories
/db.summary.distinct("category")

// Which fields are common
/db.summary.aggregate([
  { $project: { keys: { $objectToArray: "$$ROOT" } } },
  { $unwind: "$keys" },
  { $group: { _id: "$keys.k", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])








