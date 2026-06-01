from reviewer import review_code

fake_diff = """
diff --git a/app.py b/app.py
index 83db48f..f12a9c3 100644
--- a/app.py
+++ b/app.py
@@ -1,5 +1,6 @@
 def add(a, b):
-    return a + b
+    result = a + b
+    return result

 def divide(a, b):
     return a / b
"""

print(review_code(fake_diff))